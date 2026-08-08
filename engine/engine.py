#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   engine.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/06 20:31:45 by jay-k               #+#    #+#            #
#   Updated: 2026/08/08 14:59:08 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

# import sys
# import time
# import threading
# # from typing import Any
# # from data_models.connection import Connection
# from data_models.zone import Zone
# from data_models.graph import Graph
# from data_models.drones import Drone
# from algorithm.dijkstra import dijkstra


# class Engine:
#     def __init__(self, graph: Graph):
#         # creating an initiating a stat for each zone with data on
#         # zone and number of drones in that zone
#         zone_stat: dict[Zone, list[Drone]] = {}
#         # creating a drone stat with drone object in order
#         # and the path info, this can also be used to identify
#         # each drones
#         drones_stat: dict[Drone, list[Zone]] = {}

#         for zone in graph.zones:
#             if zone.coordinates == (0, 0):
#                 for a in range(0, graph.total_drones):
#                     drone = Drone()
#                     zone_stat[zone].append(drone)
#                     drones_stat[drone] = []
#             zone_stat[zone] = []

#         request: dict[Drone, Zone] = {}
#         capacity: dict[Zone, int] = {}

#         for zone in graph.zones:
#             capacity[zone] = len(zone_stat[zone])

#         blocked: list[Zone] = [
#             zone for zone in graph.zones if zone.cost != sys.maxsize]

#         def simulation(zone_stat):
#             # scanning, collecting paths and filling request and
# #             for drone in drones_stat.keys():
#                 union = list(set(blocked) | set(drone.came_from))
#                 drones_stat[drone] = dijkstra(drone, union, graph)
#                 request[drone] = drones_stat[drone][1]

#             # by now request is full and updated and drones_stat also full
#             # scheduling next executuion after 1 second
#             threading.Timer(1.0, simulation).start()

#         # start loop
#         simulation()

#         # keep the main thread alive
#         try:
#             while True:
#                 time.sleep(1)
#         except KeyboardInterrupt:
#             pass

#         def move():
#             pass
# UNCOMMENT ABOVE ALL!!!! also optimization and move
# function sorts the drones based on which one is closer to the end_hub
# should also consider priority
# @staticmethod
# def optimization(requests: list[Zone]) -> list[Zone]:
#     requests = sorted[
#       requests, key=lambda x: x[drone].coordinates, reverse=True
#     ]
#     return requests

# moves the drones: change current to next and add current to came_from

# import threading
# import time

# def run_code():
#     # Your code here
#     print(f"Running at {time.strftime('%X')}")

#     # Schedule the next execution after 1 second
#     threading.Timer(1.0, run_code).start()

# # Start the loop
# run_code()

# # Keep the main thread alive
# try:
#     while True:
#         time.sleep(1)
# except KeyboardInterrupt:
#     pass


# You are basically thinking:

# Engine
#  |
#  |-- keeps global time
#  |-- keeps zone occupancy
#  |-- keeps connection occupancy
#  |-- asks each drone: "what is your next move?"
#  |
#  v
# Dijkstra
#  |
#  |-- calculates possible path
#  |-- does not manage time
#  |-- does not move drones

# That separation is good.

# Your engine tick could conceptually look like:

# time += 1

# for each drone:
#     path = dijkstra(drone, zone_stat, graph)
#     next_zone = path[1]

# check all requested moves:
#     is zone capacity available?
#     is connection capacity available?

# allow:
#     move drone

# deny:
#     drone waits

# The important part is:

# Don't move drones immediately while calculating.

# Because of multiple drones.

# Example:

# Zone B capacity = 1

# Drone A wants:
# A -> B

# Drone C wants:
# C -> B

# If you process A first:

# B = occupied

# then C gets rejected.

# But if C was processed first, A gets rejected.

# That means the order of your loop changes the simulation result.

# A better pattern:

# Phase 1: Planning

# Every drone says:

# Drone 1:
# current = A
# wants = B

# Drone 2:
# current = C
# wants = B

# Store:

# requests = {
#     drone1: B,
#     drone2: B
# }

# No movement yet.

# Phase 2: Validation

# Engine checks:

# How many drones want B?

# capacity(B) = 1
# requests(B) = 2

# Then decide:

# Drone 1 moves
# Drone 2 waits

# (or use priority rules)

# Phase 3: Commit movement

# Only now:

# drone.current_zone = next_zone
# zone_stat[next_zone] += 1

# This also solves your connection capacity problem.

# Example:

# A ===== B
# connection capacity = 1

# Requests:

# Drone1: A -> B
# Drone2: B -> A

# The engine decides who uses the connection.

# One thing I would reconsider though:

# Your Dijkstra currently has:

# zone.cost

# but your engine idea means cost is dynamic.

# Maybe eventually:

# total_cost = (
#     zone.cost
#     + waiting_time(zone)
#     + waiting_time(connection)
# )

# But don't put this in Engine. Let Dijkstra ask the engine/state:

# "How expensive is moving from A to B at this moment?"

# Something like a cost callback.

# Your design is actually close to how traffic
#  simulations and robot fleet systems are designed:

# Path planner → "where should I go?"
# Simulator/controller → "can I go now?"

# Keeping them separate will save you a lot of pain later. Your instinct
# to make an Engine class is a good one.
