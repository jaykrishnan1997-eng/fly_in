# Day 1 (Phase1)

- Read subject, understand basically how things should be. 
- The use of AI must be for research, resources and planning only.
- A plan was made using Clause, saved as references.md
- Also used AI to make a pre-commit config so that only flake8 and mypy code can be commited. This is made as a git config.
- this file process will document my process in understanding.
- [mpouillo/42-fly-in](https://github.com/mpouillo/42-fly-in), ran this, also learned the algorithm fundamentaly mentioned via youtube and g4g
- Starting parsing, map is the config!
- Another well structured reference : (https://github.com/sergioromero2k/42_Fly-in_v1.4). Project/Folder structure inspired.
- From claude i understand Zone need a class that accepts name, type, capacity, extra metadata.
- Drone needs ID, current position, destination-properties
- Connection needs node a, node b and capacity

# Day 2

- Started class zone also included x, y, color and a seld describing method
- started class graph with list of zones, connections and start, stop zones, and total number of drones.
- Started class connections with zone_a, zone_b, max_drones.
- started parsing class, also made sure git has numbpy and flake8 check
-  pre-commit --version
  pre-commit install
  pre-commit run --all-files

  # Day 3

  - Diving into parser: started with the simple map. Parsing every sing content of map into graph object.
  - There was a choice to parse and collect all the hub info together to make the code simpler. But as a safety precaution, i need to make sure the Zones list is sorted based on the coordinates.
  - Also made the x, y coordinates into a tuple for ease of sorting the zones(probably unnecissary)
  - Asked "python sort coordinates tuple from class elements" to gemini.
  - Asked gemini if a compress of this python statement is possible :if new_connection in connections or rev_connection in connections :
 - added init.py in every packages since import caused error of not recognizing file names.
 - chatgpt for error handling and corrections. Must learn to debug properly.
 - Fixed the error on dispplay stats. Capable of handling even the challenger txt
 - example output:
 
 ┬─[jkrishna@2-H-9:~/C/L/fly-in]─[02:10:23 PM]─[G:master=]
╰─>$ python3 main.py maps/easy/01_linear_path.txt
Graph: 4 zones and 3 connections

Start zone: name: start
coordinates: (0, 0)
type: normal
color: green
maximum occupancy: 2

end zone: name: goal
coordinates: (3, 0)
type: normal
color: red
maximum occupancy: 2

Total drones: 2

┬─[jkrishna@2-H-9:~/C/L/fly-in]─[02:10:34 PM]─[G:master=]
╰─>$ python3 main.py maps/challenger/01_the_impossible_dream.txt
Graph: 54 zones and 70 connections

Start zone: name: start
coordinates: (0, 0)
type: normal
color: green
maximum occupancy: 25

end zone: name: impossible_goal
coordinates: (21, 0)
type: normal
color: rainbow
maximum occupancy: 25

Total drones: 25


 # Day 4 (Phase2)

 - started Dijkstras : choosing method over a alg class. Return is a dict for str and dict.
 -  refer : https://youtu.be/bZkzH5x0SKU
 - case: starting to think about just one drone finding path
 - What is cost for every connection? And how should it be calculated in decided based on zones?
 - starting with simple easy case. 
 - Trial1: cost of connection is cost of the endpoint zone.
 Two cost should be there one for number of turns and one for no of drones possible
 - A new class called drones was created to hold current zone and the list returned by algorithm. Slightly over kill but looks better and easy to create an instance in engine.
 - TO DO: Just one drone, make algorithm to move from start to end based on cost. Stat and alg every run untill all drone in end hub.

 # Day 5

 - Asked claude what a cost calculation mean in the flyin and what and how a heapq works, deque works and the typing format for return.
 - Just like traversing a list or the kruskal in A-maze-ing, i remade a python alg of Dijkstras. Bit complicated.
 - The zone occupied condition havent been implemented yet. As said before, just one drone in my mind.
 - Asked claude to suggest better option to handle the cost_stat table, with dict or with dataclass. dict was chosen with list replaced by tuple. access to tuple and list feels almost the same except if i need to update an elemenrt inside the tuple i need to update both. 
 - heap wasnt supposed to be reset every step it is supposed to collect the chains posible. That is, heap should be outside the while loop.
 - resetting: dijkstra. Claude was used for understanding exactly how heap and cost_stat are used in dijkstra. Also the logic had confusion and AI was used to understand them and to clarify doubt.
 - heapq is still confusing. lots of mypy error and logic errors. I did use clause for understanding logic issues in the algorithm. Right now it seemd working.

 # Day 6

 - starting with engine. Asked chatgpt for the best design choice and choose to keep engine separately for time movement and occupancy calc. Like traffic : engine and google map : alg for each vehicle.
 - using function within function so that i can hold data in the outside function during every tick.
 - Learned to take union of two list from : https://www.pythonpool.com/python-union-of-lists/
 - include optimization and move functions to optimise or sort based on closeness to endpoint and move based on capacity.
 - used google ai to understand how sorted function works, I forgot
 - To do: remove drone_stat: class itself is capable of containing the path forward

 # Day 7[Aug 10] Kind of (Phase3)

 - Kind of moving from single drone to multidrone case for simulation since its all the same.
 - lot of confusion on the implementation. with multiple stats and how to update them. Claude was used for checking the correctness and bugs, and asked doubts on sorted function.
 - Now the drones when on transit must wait. So how can i include that also while making a move.
 - Drones was updated to include transit info when transiting through connection. This is better than choosing a seperate class. Now must include transit and update transit into code when zone is restricted.

 # Day 8[Aug 12]

 - icorporating drone transit info into the engine. Q. Where all should i include it on next_move and in move.
 - made sure to include the branch for transit in move, simulation and next_move. Also updated graph to include get_connnection and bit more additions:

 # status:  Resolved / traced correct:

 - Zone/Connection/Drone/Graph/Parser classes — done
 - Dijkstra core algorithm — heap persistence, tuple pushes, cost accumulation, finalized-zone handling all fixed
 - Zone-type cost mapping (normal=1, priority=1, restricted=2, blocked=impassable) — clarified against spec
 - Restricted-zone transit mechanic (start_transit/update_transit on Drone) — timing fixed (1 turn_remaining, single update_transit() call lands correctly)
 - Engine.next_move() — distinguishes normal moves vs. transit-start vs. already-transiting drones; capacity/occupancy bookkeeping for each case
 - Engine.move() — three branches (direct move, start transit, complete transit) all wired to update zone_stat, connection_stat, and drones_stat consistently
 - Engine.simulation() — skips redundant dijkstra() recompute for drones mid-transit

  # Not yet checked/still open:

  - No actual end-to-end run against a real map file yet — everything so far has been traced by hand/logically, not executed
  next_move()'s priority sorting (abs_distance from start hub) — - - functionally wired, but worth confirming it's actually the tiebreak/prioritization behavior you want under real contention
  - The run() / threading.Timer real-time-loop design — flagged early on as a bigger design question (real-time delay vs. synchronous turn loop) that hasn't been revisited
  - Zone occupancy edge cases from the spec (start/end zone exceptions, max_drones at non-default zones) — not specifically traced yet
  - Output format (D<ID>-<zone> / D<ID>-<connection> turn log) — no code for this yet, per what's been shown
  - Parser error handling completeness (line numbers, all invalid-input cases) — not touched in recent messages
  Visual representation (terminal/graphical) — not started
  - Tests — not started
  - README — not started

 # #########################
 # Doomsday

 - The sun is down. My device battery is low. I dont know how long i can keep myself alive. Tell my future wife and kids that i love them.
