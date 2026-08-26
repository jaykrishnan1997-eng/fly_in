*This project has been created as part of the 42 curriculum by jkrishna.*

# Fly-in — Drone Traffic Simulation

## Description

Fly-in is a turn-based simulation that routes a fleet of drones from a shared
`start` zone to a shared `end` zone across a custom-built graph of zones and
connections, while respecting per-zone occupancy limits, per-connection
capacity limits, and per-zone-type movement costs (`normal`, `priority`,
`restricted`, `blocked`).

The goal is to move every drone from start to goal in as few simulation
turns as possible, without ever violating a capacity constraint or a
movement rule, and to make the resulting simulation observable through a
live visual dashboard.

The project is built entirely from scratch: the graph structure, the parser
for the custom map file format, the turn-based simulation engine, and the
pathfinding algorithm are all custom implementations — no graph libraries
(e.g. `networkx`, `graphlib`) are used, per the subject's constraints.

## Instructions

### Requirements

- Python 3.10+
- [`uv`](https://docs.astral.sh/uv/) for dependency management (or `pip`,
  see `pyproject.toml` for the dependency list)

### Install

```bash
make install
```

This creates a virtual environment (`.venv`) and installs all dependencies
(`rich`, `textual`, `flake8`, `mypy`, etc.) via `uv sync`.

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

This launches the Textual dashboard, which starts the simulation and steps
it forward automatically (one tick per second by default).


### Controls (inside the dashboard)

| Key | Action |
|-----|--------|
| `p` | Pause / resume the simulation |
| `s` | Step forward one tick manually |
| `m` | Open the map selector and switch maps |
| `r` | Restart the current map |
| `q` | Quit |

### Debug / development

```bash
make debug     # run with Python's built-in debugger (pdb)
make lint      # flake8 + mypy (subject-mandated flags)
make lint-strict  # flake8 + mypy --strict
make clean     # remove __pycache__, .mypy_cache, etc.
```

## Algorithm Explanation

### Graph & Parser

`Zone`, `Connection`, `Drone`, and `Graph` are custom classes built without
any graph library. The parser (`parser/map_parser.py`) reads the map's
custom text format line by line, validates zone types, coordinates,
metadata (`max_drones`, `max_link_capacity`, `color`), and connection
definitions, and raises a descriptive `ValueError` on malformed input.

Before the simulation starts, `Engine.is_reachable()` runs a BFS from
`start_hub` to `end_hub` (skipping `blocked` zones) to fail fast with a
clear error if the map has no valid path at all.

### Pathfinding: per-drone Dijkstra

Each drone's route is computed independently with a custom Dijkstra
implementation (`algorithm/dijkstra.py`), using a binary heap
(`heapq`) keyed on accumulated zone cost. Zone-type costs follow the
subject's rules:

| Zone type | Cost (turns) |
|---|---|
| `normal` | 1 |
| `priority` | 1 (preferred by the cost function) |
| `restricted` | 2 |
| `blocked` | unreachable (excluded from the graph search) |

A drone's own visited-zone history (`came_from`) is excluded from its own
future searches to avoid trivial backtracking loops.

### Turn-based scheduling: `next_move()` / `move()`

Each tick, `Engine.next_move()` computes, for every drone not currently
mid-transit, whether its next planned hop is available this turn:

- **Zone occupancy check**: `zone_occupancy - zone_outgoing < zone.max_drones`
  — a zone's outgoing drones free up capacity in the *same* tick they leave,
  matching the subject's "drones moving out of a zone free up capacity for
  that same turn" rule.
- **Connection capacity check**: a connection's capacity is similarly
  discounted for drones whose restricted-zone transit is completing
  (`turns_remaining <= 1`) this same tick, so a connection frees up the
  instant a drone lands, rather than one tick late.
- If a drone's planned hop is blocked (zone full, connection full, or
  another drone already claimed that zone this tick), the drone triggers a
  **local reroute**: a fresh Dijkstra search excluding the blocked
  connection, to try an alternative path immediately.

`Engine.move()` then applies every approved move: direct one-turn hops,
starting a multi-turn restricted-zone transit (`Drone.start_transit()`),
or completing one (`Drone.update_transit()`), updating `zone_stat`,
`connection_stat`, and each drone's remaining path (`drones_stat`)
consistently.

### Known limitation: no lookahead beyond the next hop

The reroute logic above only reacts to *immediate* contention — it has no
way to know whether waiting one or two ticks for a busy zone to clear would
be faster than taking a valid but much longer detour. On maps with dead
ends and loops specifically designed to punish this (e.g. `Hard Level 1`),
this can occasionally send a drone on an unnecessarily long detour instead
of simply waiting.

The theoretically correct fix for globally optimal throughput is a
**max-flow approach over a time-expanded graph** (e.g. Ford-Fulkerson /
Edmonds-Karp): duplicating the graph once per tick and solving for maximum
flow across the whole time-expanded network at once, rather than routing
each drone greedily and independently. This was identified as the right
direction during peer evaluation but was not implemented, as it is a
different algorithmic approach rather than a tunable extension of the
current per-drone Dijkstra design.

### Complexity

- Each per-drone Dijkstra run is `O((V + E) log V)` with the binary heap.
- Recomputing a path for every non-transiting drone every tick gives a
  worst case of roughly `O(D * (V + E) log V)` per tick, where `D` is the
  number of drones — acceptable for the map sizes used here (up to ~54
  zones, 25 drones on the Challenger map), but would not scale gracefully
  to very large graphs or drone counts without caching/memoization.

## Visual Representation

The dashboard is built with [Textual](https://textual.textualize.io/)
(migrated from an earlier Rich-only prototype) and is composed of five
live-updating panels:

- **Airspace Map** — a custom ASCII-canvas rendering of the graph: zones
  are drawn as symbols (`S`/`E` for start/end, `R` for restricted, `P` for
  priority, `B` for blocked, `U` for normal) at positions scaled from their
  map coordinates, connections are drawn as lines between them, and drones
  are drawn as `D<ID>` labels that visually interpolate between zones while
  mid-transit. Hovering the mouse over a zone shows a popup with its
  name, cost, live occupancy, and coordinates — useful for inspecting
  larger/denser maps where zone names would otherwise clutter the canvas.
- **Event Log** — the turn-by-turn movement log (`D<ID>-<zone>` /
  `D<ID>-<connection>`), and, when `--capacity-info` is enabled, live
  per-zone and per-connection capacity usage.
- **Drone Table** — every drone's current zone, remaining path, status
  (`IN_TRANSIT` / `IN_END_ZONE`), and whether it's currently waiting.
- **Summary** — aggregate simulation statistics: total drones, drones in
  connections/transit, completed drones, total path cost, and total turns.
- **Map Selector** — a modal screen (`m` key) to switch between any `.txt`
  map file under `maps/` without restarting the program.

Colors specified in the map file's `[color=...]` metadata are parsed and
applied to each zone's rendered symbol, so the visual map reflects the
map author's own zone-type/color scheme rather than a fixed palette.

## Example Input & Expected Output

Input (`maps/easy/02_simple_fork.txt`):

```
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

Expected output (event log, one line per turn):

```
D1-junction D2-junction
D1-path_a D3-junction
D1-goal D2-path_b D3-path_a
D2-goal D3-goal
```

Drones D1 and D2 are automatically split across `path_a` and `path_b`
(equal-cost alternatives) once `junction`'s capacity is reached, rather
than queuing behind each other on a single path.

## Resources

### Documentation & references used

- [Rich documentation](https://rich.readthedocs.io/) — `Layout`, `Panel`,
  `Text` styling (early prototype, later migrated away from)
- [Textual documentation](https://textual.textualize.io/) — widgets,
  `App`/`Screen` composition, CSS-like styling, generics (`App[T]`,
  `DataTable[T]`)
- [Rich Layout Docs](https://rich.readthedocs.io/en/latest/layout.html)
- Rich FullScreen example (willmcgugan/rich, GitHub)
- Dijkstra's algorithm — general algorithm reference via freeCodeCamp /
  GeeksforGeeks, and a walkthrough video
  ([youtu.be/bZkzH5x0SKU](https://youtu.be/bZkzH5x0SKU))
- Rich `Layout` walkthrough video
  ([youtu.be/NoYZtYBiYbo](https://youtu.be/NoYZtYBiYbo))
- [mpouillo/42-fly-in](https://github.com/mpouillo/42-fly-in) and
  [sergioromero2k/42_Fly-in_v1.4](https://github.com/sergioromero2k/42_Fly-in_v1.4)
  — read for general project-structure inspiration before writing any code
- [Python union of two lists — pythonpool.com](https://www.pythonpool.com/python-union-of-lists/)

### AI usage

AI (Claude, ChatGPT, Gemini) was used as a development and learning
assistant, not as a code generator that wrote the project. It was used to
explain unfamiliar Python/library behavior (`heapq`, `deque`, typing
generics, Textual's widget/CSS model), help diagnose real errors and bugs
from my own terminal output and event logs (mypy/Textual issues, capacity
and scheduling bugs), reason through algorithm design decisions (Dijkstra
cost functions, occupancy/capacity tracking), and identify a known
limitation in the current pathfinding approach (documented above). All
code was written, integrated, and tested by hand against real map files;
AI-suggested changes were verified with `mypy --strict`, `flake8`, and the
simulation output before being kept. A day-by-day development log is
available in `progress.md`.
