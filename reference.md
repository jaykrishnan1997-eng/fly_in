# Fly-in Project — Plan & References

## Reality Check on Scope

The reference implementation (full 3D raylib, first-person view, time-travel scrubbing) represents way more than 120 hours for a solo dev on top of the core logic. Evaluation cares most about:

- Correct parsing
- Correct pathfinding under constraints
- Correct capacity/collision handling
- *Some* visual feedback — not how flashy it is

Terminal or simple 2D output satisfies the requirement. Treat 3D as a stretch goal only if everything else is done and tested with time to spare.

---

## Phase Breakdown (120h)

### Phase 1 — Parsing & Data Model (≈20h)
- Design classes first: `Zone`, `Connection`, `Drone`, `Map`/`Graph`. Get the OOP structure right before writing logic — this project explicitly grades on being "completely object-oriented."
- Write the map file parser: `nb_drones`, `start_hub`/`end_hub`, zone metadata blocks, connection syntax, capacity values.
- Build out every error case the spec lists (invalid zone type, duplicate connections, malformed metadata, bad capacity values) with line-number error messages. This is graded and easy to half-do — don't leave it for later.
- Set up `mypy --strict` and `flake8` from commit #1, not bolted on at the end.

### Phase 2 — Core Pathfinding (≈25h)
- Implement Dijkstra by hand (no `networkx`/`graphlib`). Decide your adjacency representation early (adjacency list keyed by zone name is simplest).
- Encode zone-type weighting:
  - `restricted` = 2-turn cost
  - `priority` = preferred (lower weight)
  - `blocked` = excluded entirely
- Get single-drone pathfinding correct and tested before touching multi-drone logic.

### Phase 3 — Multi-Drone Simulation (≈30h)
- The hardest part: simultaneous movement, per-turn capacity constraints on zones and connections, drones re-pathing every turn when blocked.
- Implement a turn-by-turn simulation loop: each drone recomputes its path each turn, respects `max_drones`/`max_link_capacity`, and the restricted-zone "must arrive next turn" rule.
- Test with small hand-crafted maps first (2–3 drones, a fork, a bottleneck) before anything complex — this is where subtle bugs hide.

### Phase 4 — Output & Visualization (≈20h)
- Do the required step-by-step turn log first (`D<ID>-<zone>` format) — satisfies the "output" requirement and is needed for debugging anyway.
- Then add visual feedback. Start with simple terminal/ASCII rendering of zones and drone positions per turn — cheap, satisfies the spec, and gives you something to demo even if you run out of time.
- Only reach for pygame/raylib if Phases 1–3 are solid with buffer left. A working terminal viz beats a half-built 3D one.

### Phase 5 — Edge Cases, Testing, Defense Prep (≈20h)
- Test with maps that have no valid path, disconnected zones, zero-capacity edge cases, single drone, many drones through one bottleneck.
- Re-read the spec line by line against your implementation — 42 defenses catch exactly the constraint you skipped.
- Prepare to explain your Dijkstra modification and design choices out loud; defenses usually probe algorithm reasoning more than code style.

### Buffer (≈5h)
Leave unscheduled. Something in Phase 3 will take longer than planned — it always does.

---

## Sequencing Advice

Don't parallelize Phases 1–3 — each depends on the last being solid. Resist starting with the graphical layer first (tempting, since it's visually satisfying): it's the one part of the spec that's flexible in implementation, while parsing/pathfinding/capacity logic is precisely specified and graded. Get the unglamorous stuff bulletproof first.

---

## References

### Algorithm — Dijkstra Core
- [Dijkstra's Algorithm (GeeksforGeeks)](https://www.geeksforgeeks.org/dsa/dijkstras-algorithm-for-adjacency-list-representation-greedy-algo-8/) — clean adjacency-list implementation walkthrough
- [Dijkstra visual explainer (YouTube)](https://www.youtube.com/watch?v=bZkzH5x0SKU) — good for building intuition before coding
- [Representing graphs in Python (Stack Overflow)](https://stackoverflow.com/questions/19472530/representing-graphs-data-structure-in-python) — adjacency-list vs matrix vs dict-of-sets, relevant since `networkx` is banned

### Multi-Drone / Capacity-Constrained Movement
The simplest correct approach — and the one the reference implementation uses — is **per-turn re-Dijkstra with dynamic edge weighting** (add cost/blocking to zones occupied by other drones that turn), rather than a full cooperative-pathfinding algorithm. This stays within the OOP + no-graph-library constraints and is far easier to get right in a 120h budget.

- [Cooperative Pathfinding, D. Silver (2005)](https://arxiv.org/pdf/1911.07840) — the original simple/practical formulation this problem descends from; worth 20 minutes for the theory behind why naive simultaneous planning creates deadlocks
- **Avoid the Conflict-Based Search (CBS) rabbit hole** unless Phase 3 is done early with time to spare — it's the "correct" academic solution but significant extra complexity for marginal benefit here

### Python Typing & OOP Discipline
- [mypy documentation](https://mypy.readthedocs.io/en/stable/) — strict mode reference, since the spec requires full typesafety
- [flake8 documentation](https://flake8.pycqa.org/)

### Visualization (once core logic is done)
- **Terminal-first**: plain `print()` grid rendering per turn is enough to satisfy the spec — no library needed
- **If 2D**: [pygame docs](https://www.pygame.org/docs/) — simpler to pick up fast than raylib
- **If 3D** (only with spare time): [Raylib cheatsheet](https://www.raylib.com/cheatsheet/cheatsheet.html) and [Python bindings docs](https://electronstudio.github.io/raylib-python-cffi/index.html) — highest-cost/lowest-grading-value part of the project

### Worked Reference Implementation
- [mpouillo/42-fly-in](https://github.com/mpouillo/42-fly-in) — a completed student implementation with map file examples, project structure, and a writeup of their Dijkstra adaptation. Useful for sanity-checking parsing rules and turn-log format — don't copy the 3D scope.