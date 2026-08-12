#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   engine.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/06 20:31:45 by jay-k               #+#    #+#            #
#   Updated: 2026/08/12 14:53:23 by jkrishna           ###   ########.fr      #
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
        if len(self.zone_stat[self.graph.end_hub]) == len(self.drones_stat):
            print("OK")
            sys.exit()
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
