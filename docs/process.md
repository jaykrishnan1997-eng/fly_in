# Day 1

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