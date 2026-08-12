#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   engine.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/06 20:31:45 by jay-k               #+#    #+#            #
#   Updated: 2026/08/12 14:30:40 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import sys
import time
import math
import threading
from collections import deque
from data_models.zone import Zone
from data_models.graph import Graph
from data_models.drones import Drone
from algorithm.dijkstra import dijkstra
from data_models.connection import Connection


class Engine:
    def __init__(self, graph: Graph):
        self.graph = graph

        self.zone_stat: dict[Zone, list[Drone]] = {}
        self.drones_stat: dict[Drone, deque[Zone]] = {}
        self.connection_stat: dict[Connection, list[Drone]] = {}
        self.zone_outgoing: dict[Zone, int] = {}

        for zone in self.graph.zones:
            if zone == self.graph.start_hub:
                self.zone_stat[zone] = []
                for a in range(0, self.graph.total_drones):
                    drone = Drone(self.graph.start_hub, [])
                    self.zone_stat[zone].append(drone)
                    self.drones_stat[drone] = deque()
            else:
                self.zone_stat[zone] = []
        for connection in self.graph.connections:
            self.connection_stat[connection] = []
        self.request: dict[Drone, Zone] = {}
        self.zone_occupancy: dict[Zone, int] = {}
        self.connection_capacity: dict[Connection, int] = {}

        self.blocked: list[Zone] = [
            zone for zone in self.graph.zones if zone.cost != sys.maxsize]

    def next_move(self) -> None:
        self.request = {}

        self.zone_outgoing = {
            zone: 0
            for zone in self.graph.zones
        }

        self.zone_occupancy = {
            zone: len(self.zone_stat[zone])
            for zone in self.graph.zones
        }

        self.connection_capacity = {
            connection: len(self.connection_stat[connection])
            for connection in self.graph.connections
        }
        # optimization, further one more priority
        drones = sorted(
            self.drones_stat.keys(),
            key=lambda drone: self.abs_distance(
                drone.current_zone.coordinates[0],
                drone.current_zone.coordinates[1]), reverse=True
        )

        for drone in drones:
            if len(self.drones_stat[drone]) <= 1:
                # drone at destination
                continue

            next_zone = self.drones_stat[drone][1]
            current_zone = drone.current_zone
            connection = self.graph.get_connection(current_zone, next_zone)

            if (
                ((
                    self.zone_occupancy[next_zone]
                    - self.zone_outgoing[next_zone])
                    < next_zone.max_drones)
                and connection
                and self.connection_capacity[connection]
                < connection.max_link_capacity
            ):
                # normal transit
                if next_zone.cost == 1:
                    self.request[drone] = next_zone
                    self.zone_occupancy[next_zone] += 1
                    self.zone_outgoing[current_zone] += 1
                    self.connection_capacity[connection] += 1

                # special transit
                elif next_zone.cost < sys.maxsize and next_zone.cost > 1:
                    # towars the destination
                    if drone.current_connection is None:
                        self.request[drone] = next_zone
                        self.zone_outgoing[current_zone] += 1
                        self.connection_capacity[connection] += 1
                        self.connection_stat[connection].append(drone)

                    # towards the connection
                    else:
                        self.request[drone] = next_zone
                        self.zone_occupancy[next_zone] += 1
                        self.zone_outgoing[current_zone] += 1
                        # self.connection_capacity[connection] -= 1
                        # self.connection_stat[connection].remove(drone)

    def move(self) -> None:
        # transit_drones = []
        # for transit in self.connection_stat.values():
        #     for d in transit:
        #         transit_drones.append(d)

        for drone in self.request.keys():
            expense = self.drones_stat[drone][1].cost
            self.zone_stat[drone.current_zone].remove(drone)
            drone.came_from.append(drone.current_zone)

            # cost 1: direct transit
            if expense == 1:
                drone.current_zone = self.request[drone]
                self.zone_stat[drone.current_zone].append(drone)
                self.drones_stat[drone].popleft()

            # transit into the connection
            elif (
                expense > 1
                and expense < sys.maxsize
                and drone.current_connection is None
            ):
                # this will start transit, set current_connection and
                # set destination
                connection = self.graph.get_connection(
                        drone.current_zone, self.request[drone])
                if connection is not None:
                    drone.start_transit(connection, self.request[drone])
                    self.connection_stat[connection].append(drone)
                else:
                    raise ValueError
            # transit from connection into the destination zone
            else:
                drone.update_transit()
                if drone.current_connection is None:
                    self.zone_stat[drone.current_zone].append(drone)
                    self.drones_stat[drone].popleft()

    def simulation(self) -> None:
        # scanning, collecting paths and filling request and
        for drone in self.drones_stat.keys():
            if drone.current_connection is None:
                union = list(set(self.blocked) | set(drone.came_from))
                self.drones_stat[drone] = deque(
                    dijkstra(drone, union, self.graph)
                    )
        # update all next moves, check based on availability
        self.next_move()

        # now move
        self.move()
        # by now request is full and updated and drones_stat also full
        # scheduling next executuion after 1 second
        threading.Timer(1.0, self.simulation).start()

    def run(self) -> None:
        # start loop
        self.simulation()

        # keep the main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass

        # zone_occupancy is temporary. zone stat is permanent.
        # where i create the optimized requests before the move

    def abs_distance(self, x: int, y: int) -> float:
        return (
            math.sqrt(
                (x - self.graph.start_hub.coordinates[0])**2 +
                (y - self.graph.start_hub.coordinates[1])**2
            ))

    # def optimization(self) -> None:
    #     self.request = dict(sorted(
    #         self.request.items(),
    #         key=lambda x: self.abs_distance(
    #             x[0].current_zone.coordinates[0],
    #             x[0].current_zone.coordinates[1]), reverse=True
    #     ))
# s
# s
# s
# s
# s
# s
# s
# s
# s
# s
# s
# s
# s
# s
# s
# s
# s
# s
# s
# s
# s
# s
# s
# s
# s
# s
# s
# s

# UNCOMMENT ABOVE ALL!!!! also optimization and move
# function sorts the drones based on which one is closer to the end_hub
# should also consider priority

# moves the drones: change current to next and add current to came_from

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
#     is zone zone_occupancy available?
#     is connection zone_occupancy available?

# allow:
#     move drone

# deny:
#     drone waits

# The important part is:

# Don't move drones immediately while calculating.

# Because of multiple drones.

# Example:

# Zone B zone_occupancy = 1

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

# zone_occupancy(B) = 1
# requests(B) = 2

# Then decide:

# Drone 1 moves
# Drone 2 waits

# (or use priority rules)

# Phase 3: Commit movement

# Only now:

# drone.current_zone = next_zone
# zone_stat[next_zone] += 1

# This also solves your connection zone_occupancy problem.

# Example:

# A ===== B
# connection zone_occupancy = 1

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
