# Fly-in — Drone Traffic Simulation

*This project has been created as part of the 42 curriculum by jkrishna.*

## Description

Fly-in is a turn-based simulation that routes a fleet of drones from a shared `start` zone to a shared `end` zone across a custom-built graph of zones and connections.

The simulation respects per-zone occupancy limits, per-connection capacity limits, and per-zone-type movement costs (`normal`, `priority`, `restricted`, `blocked`).

The goal is to move every drone from start to goal while respecting the movement and capacity constraints of the map. The resulting simulation can be observed through a live interactive dashboard.

The project is built from scratch: the graph structure, parser for the custom map format, simulation engine, and pathfinding algorithm are custom implementations. No external graph libraries such as `networkx` are used.

## Instructions

### Requirements

- Python `>=3.12,<3.13`
- [`uv`](https://docs.astral.sh/uv/) for dependency management
  (or `pip`; see `pyproject.toml` for the dependency list)

### Install

```bash
make install
```

This creates a virtual environment (`.venv`) and installs the project dependencies through `uv sync`.

### Run

```bash
make run
```

or directly:

```bash
python3 main.py maps/<difficulty>/<map_file>.txt
```

Example:

```bash
python3 main.py maps/easy/01_linear_path.txt
```

This launches the Textual dashboard and advances the simulation automatically at its configured refresh interval.

### Controls

| Key | Action |
|-----|--------|
| `p` | Pause / resume the simulation |
| `s` | Step the simulation forward manually |
| `m` | Open the map selector and switch maps |
| `r` | Restart the current map |
| `q` | Quit |

### Debug / development

```bash
make debug          # run with Python's built-in debugger (pdb)
make lint           # run flake8 and mypy
make lint-strict    # run flake8 and mypy --strict
make clean          # remove __pycache__, .mypy_cache, etc.
```

## Algorithm Explanation

### Graph & Parser

`Zone`, `Connection`, `Drone`, and `Graph` are custom classes built without an external graph library.

The parser (`parser/map_parser.py`) reads the custom map format line by line. It validates:

- the number of drones
- zone and hub definitions
- coordinates
- zone types
- zone metadata
- zone occupancy limits
- connection definitions
- connection capacity limits
- duplicate connections
- references to unknown zones
- the presence of the start and end hubs

Supported zone metadata includes:

```text
[zone=normal]
[color=green]
[max_drones=2]
```

Connection metadata can specify:

```text
[max_link_capacity=2]
```

Malformed map definitions raise descriptive `ValueError` exceptions.

Before the simulation starts, `Engine.is_reachable()` checks that the end hub can be reached from the start hub while excluding blocked zones. This allows invalid maps with no usable route to fail before the simulation begins.

### Pathfinding: Per-drone Dijkstra

Each drone can calculate a route using a custom Dijkstra implementation (`algorithm/dijkstra.py`).

The implementation uses Python's `heapq` as a priority queue and calculates routes according to the movement costs of the zones:

| Zone type | Movement cost |
|---|---:|
| `normal` | 1 |
| `priority` | 1 |
| `restricted` | 2 |
| `blocked` | unreachable |

`priority` zones have the same movement cost as normal zones but carry a separate priority value used by the project when making routing decisions.

Blocked zones are excluded from usable routes.

When a drone needs a new route because its planned movement cannot currently be performed, the engine can run Dijkstra again while excluding the blocked connection. This provides a local alternative route without replacing the overall scheduling system with a global optimization algorithm.

### Turn-based Scheduling: `next_move()` / `move()`

The simulation engine separates deciding which drones may move from applying those movements.

During each simulation turn, `Engine.next_move()` evaluates the next movement of drones that are able to move.

The scheduler considers:

- zone occupancy
- outgoing drones
- connection capacity
- other drones requesting the same destination
- drones currently travelling through restricted zones

When a drone leaves a zone during the current turn, its departure is taken into account when evaluating the available capacity of that zone. Similarly, connection capacity can be freed when a drone completes its transit.

If a planned movement cannot be performed because of immediate contention, the engine can perform a local Dijkstra reroute while excluding the blocked connection.

`Engine.move()` then applies the approved movements. Depending on the route, this can mean:

- completing a normal one-turn movement
- starting a multi-turn restricted-zone transit
- updating an existing transit
- moving a drone into its next zone

The engine updates the relevant occupancy, connection, and drone state as movements are applied.

### Restricted Zones

Restricted zones have a movement cost of `2`, meaning that travelling through them takes multiple simulation turns.

The `Drone` model keeps track of the transit state, including the current connection, destination, and remaining transit time. The visual dashboard uses this information to display drones travelling between zones.

### Known Limitation: Local Rerouting

The current scheduler makes decisions based primarily on the next available movement rather than performing a complete lookahead over all future turns.

When a drone encounters immediate contention, it can reroute around the blocked connection. However, the algorithm does not globally compare every possible future schedule.

For example, on a map containing loops or dead ends, a drone may sometimes take a longer valid detour when waiting for a busy zone or connection could have produced a better overall result.

A possible approach for globally optimizing throughput would be a time-expanded network model, where the graph is expanded across simulation turns and a flow algorithm is used to model simultaneous drone movement.

This approach was not implemented because the current project uses per-drone Dijkstra combined with turn-based scheduling.

### Complexity

A single Dijkstra search using a binary heap has a complexity of approximately:

```text
O((V + E) log V)
```

where `V` is the number of zones and `E` is the number of connections.

Because the engine may recompute routes for multiple drones during the simulation, the total cost depends on the number of drones and the number of rerouting/pathfinding operations performed.

The map sizes used by the project are small enough for this approach to remain practical.

## Visual Representation

The dashboard is built with [Textual](https://textual.textualize.io/) and provides several interactive components.

### Airspace Map

The `AirspaceMap` widget renders the graph on a terminal canvas.

Zones are represented by symbols:

| Zone | Symbol |
|---|---|
| Start hub | `S` |
| End hub | `E` |
| Normal | `N` |
| Priority | `P` |
| Restricted | `R` |
| Blocked | `B` |
| Unknown | `U` |

The graph coordinates are scaled to the available terminal area so that maps of different sizes can be displayed.

Connections are drawn between zones, and drones are displayed as labels such as `D1`, `D2`, etc.

While a drone is travelling between zones, its displayed position is interpolated between the two zone coordinates.

Zone colors can be specified through map metadata and are applied to the corresponding zone symbols.

Moving the mouse near a zone displays a popup containing:

- zone name
- movement cost
- current occupancy
- maximum occupancy
- coordinates

This allows zone information to be inspected without displaying all zone names directly on the map.

### Event Log

The event log displays simulation movement information as the simulation progresses.

When capacity information is enabled, zone and connection capacity information can also be displayed.

### Drone Table

The drone table provides the current state of each drone, including its location, route, and simulation status.

### Summary

The summary displays aggregate simulation information such as:

- total number of drones
- drones currently in transit
- completed drones
- total path cost
- total simulation turns

### Map Selector

The `m` key opens a map-selection screen that allows a different `.txt` map under `maps/` to be loaded without manually restarting the program.

## Example Input

The following is an example of a map containing a fork:

```text
nb_drones: 3

start_hub: start 0 0 [color=green]

hub: junction 1 0 [color=yellow max_drones=2]

hub: path_a 2 1 [color=blue]

hub: path_b 2 -1 [color=blue]

end_hub: goal 3 0 [color=red max_drones=3]

connection: start-junction

connection: junction-path_a

connection: junction-path_b

connection: path_a-goal

connection: path_b-goal
```

This map demonstrates:

- multiple drones
- a zone with limited capacity
- two alternative routes
- connections between zones
- per-zone colors
- separate start and end hubs

The exact movement order depends on the scheduler's path selection and the state of the simulation. Multiple valid movement sequences may therefore be produced.

## Resources

### Documentation & References Used

- [Rich documentation](https://rich.readthedocs.io/) — `Layout`, `Panel`, and `Text` styling used during the earlier visual prototype
- [Textual documentation](https://textual.textualize.io/) — widgets, `App`/`Screen` composition, CSS-like styling, and `DataTable`
- [Rich Layout documentation](https://rich.readthedocs.io/en/latest/layout.html)
- Rich FullScreen example by Will McGugan on GitHub
- Dijkstra's algorithm — general algorithm references and educational material
- Dijkstra walkthrough video:
  [youtu.be/bZkzH5x0SKU](https://youtu.be/bZkzH5x0SKU)
- Rich `Layout` walkthrough video:
  [youtu.be/NoYZtYBiYbo](https://youtu.be/NoYZtYBiYbo)
- [mpouillo/42-fly-in](https://github.com/mpouillo/42-fly-in) — reviewed for general project-structure inspiration
- [sergioromero2k/42_Fly-in_v1.4](https://github.com/sergioromero2k/42_Fly-in_v1.4) — reviewed for general project-structure inspiration
- Python list-union reference material from PythonPool

### AI Usage

AI tools (Claude and ChatGPT) were used as development and learning assistants to explain unfamiliar Python and library concepts, diagnose errors from real terminal output, and discuss pathfinding, capacity, scheduling, and Textual-related issues. The project was developed and integrated manually, with AI suggestions reviewed, adapted, and verified using mypy --strict, flake8, and simulation results.