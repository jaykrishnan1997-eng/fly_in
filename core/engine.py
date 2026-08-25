#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   engine.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/06 20:31:45 by jay-k               #+#    #+#            #
#   Updated: 2026/08/25 10:35:17 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import sys
import time
import math
from collections import deque
from data_models.zone import Zone
from data_models.graph import Graph
from data_models.drones import Drone
from algorithm.dijkstra import dijkstra
from data_models.connection import Connection


class Engine:

    def __init__(self, graph: Graph):
        self.graph = graph
        self._initialize()

    def _initialize(self) -> None:
        open("debug.txt", "w").close()
        self.ticks: int = 0
        self.total_path_cost: int = 0
        self.zone_stat: dict[Zone, list[Drone]] = {}
        self.drones_stat: dict[Drone, deque[Zone]] = {}
        self.connection_stat: dict[Connection, list[Drone]] = {}
        self.zone_outgoing: dict[Zone, int] = {}

        if not self.is_reachable():
            raise ValueError("No path exists from start_hub to end_hub")

        for zone in self.graph.zones:
            if zone == self.graph.start_hub:
                self.zone_stat[zone] = []
                for a in range(0, self.graph.total_drones):
                    drone = Drone(self.graph.start_hub, [], a + 1)
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
            zone for zone in self.graph.zones if zone.cost == sys.maxsize]
        self.waiting: list[Drone] = []
        self.event_log: list[str] = []

    def is_reachable(self) -> bool:
        visited = {self.graph.start_hub}
        queue = deque([self.graph.start_hub])
        while queue:
            current = queue.popleft()
            if current == self.graph.end_hub:
                return True
            for conn in self.graph.connections:
                if conn.zone_a == current:
                    neighbor = conn.zone_b
                elif conn.zone_b == current:
                    neighbor = conn.zone_a
                else:
                    neighbor = None

                if (
                    neighbor and neighbor not in visited
                    and neighbor.cost != sys.maxsize
                ):
                    visited.add(neighbor)
                    queue.append(neighbor)
        return False

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

        for connection, drones_in_transit in self.connection_stat.items():
            for d in drones_in_transit:
                if d.turns_remaining <= 1:
                    self.connection_capacity[connection] -= 1
        # optimization, further one more priority
        drones = sorted(
            self.drones_stat.keys(),
            key=lambda drone: self.abs_distance(
                drone.current_zone.coordinates[0],
                drone.current_zone.coordinates[1]), reverse=True
        )
        # print(drones)
        for drone in drones:

            if drone.current_connection is not None:
                continue

            if len(self.drones_stat[drone]) <= 1:
                # drone at destination
                continue

            next_zone = self.drones_stat[drone][1]
            current_zone = drone.current_zone
            next_connection: Connection | None = self.graph.get_connection(
                current_zone, next_zone)

            with open("debug.txt", "a") as file:
                file.write(
                    f"D{drone.id}: {current_zone.name} -> {next_zone.name}, "
                    f"occupancy={self.zone_occupancy[next_zone]}, "
                    f"outgoing={self.zone_outgoing[next_zone]}, "
                    f"max={next_zone.max_drones}\n"
                )
            if (
                next_zone in self.request.values()
                or
                (
                    next_connection is not None
                    and self.connection_capacity[next_connection]
                    >= next_connection.max_link_capacity
                )
            ):
                alternative = dijkstra(
                    drone,
                    list(set(self.blocked) | set(drone.came_from)),
                    self.graph,
                    next_connection
                )

                if len(alternative) > 1:
                    self.drones_stat[drone] = deque(alternative)
                    next_zone = alternative[1]
                    next_connection = self.graph.get_connection(
                        current_zone,
                        next_zone
                    )

            if (
                ((
                    self.zone_occupancy[next_zone]
                    - self.zone_outgoing[next_zone])
                    < next_zone.max_drones)
                and next_connection
                and self.connection_capacity[next_connection]
                < next_connection.max_link_capacity
            ):
                # normal transit
                if next_zone.cost == 1:
                    self.request[drone] = next_zone
                    self.zone_occupancy[next_zone] += 1
                    self.zone_outgoing[current_zone] += 1
                    self.connection_capacity[next_connection] += 1

                # special transit
                elif next_zone.cost < sys.maxsize and next_zone.cost > 1:
                    # towars the destination
                    if drone.current_connection is None:
                        self.request[drone] = next_zone
                        self.zone_outgoing[current_zone] += 1
                        self.connection_capacity[next_connection] += 1
                        # self.connection_stat[connection].append(drone)

                    # towards the connection
                    else:
                        self.request[drone] = next_zone
                        self.zone_occupancy[next_zone] += 1
                        self.zone_outgoing[current_zone] += 1

    def get_movement_destination(self, drone: Drone) -> str:
        if drone.current_connection is not None:
            return drone.current_connection.name

        return drone.current_zone.name

    def move(self) -> dict[Drone, str]:
        # import pdb
        # pdb.set_trace()
        self.waiting = []
        movements = {}
        for drone in self.drones_stat.keys():
            if drone.current_connection is not None:
                destination = drone.destination
                drone.update_transit()

                if drone.current_connection is None:
                    self.zone_stat[drone.current_zone].append(drone)
                    self.drones_stat[drone].popleft()

                    connection = self.graph.get_connection(
                        drone.came_from[-1],
                        drone.current_zone
                    )

                    if connection is not None:
                        self.connection_stat[connection].remove(drone)

                    if destination is not None:
                        movements[drone] = drone.current_zone.name

        for drone in self.request.keys():
            expense = self.drones_stat[drone][1].cost

            self.total_path_cost += expense

            self.zone_stat[drone.current_zone].remove(drone)
            drone.came_from.append(drone.current_zone)

            # cost 1: direct transit
            if expense == 1:
                destination = self.request[drone]

                drone.current_zone = destination

                drone.previous_zone = destination
                drone.visual_destination = None
                drone.visual_progress = 0.0

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
                    raise ValueError(
                        f"No connection from {drone.current_zone.name} "
                        f"to {self.request[drone].name}"
                    )
            movements[drone] = self.get_movement_destination(drone)

        for drone in self.drones_stat:
            if drone not in self.request:
                self.waiting.append(drone)

        # update zone occupancy after all movements
        self.zone_occupancy = {
            zone: len(self.zone_stat[zone])
            for zone in self.graph.zones
        }
        return movements

    # def print_turn(self, movements: dict[Drone, str]) -> None:
    #     output = []

    #     for drone, destination in movements.items():
    #         output.append(f"D{drone.id}-{destination}")

    #     print(" ".join(output))

    def is_finished(self) -> bool:
        return (
            len(self.zone_stat[self.graph.end_hub])
            == len(self.drones_stat)
        )

    def simulation(self) -> None:

        for drone in self.drones_stat.keys():
            if drone.current_connection is None:
                union = list(set(self.blocked) | set(drone.came_from))
                path = dijkstra(drone, union, self.graph)

                self.drones_stat[drone] = deque(path)

        self.next_move()

        movements = self.move()

        if movements:
            self.ticks += 1
            self.event_log.append(
                " ".join(
                    f"D{drone.id}-{destination}"
                    for drone, destination in movements.items()
                )
            )
            self.save_event_log()

        # self.print_turn(movements)

    def save_event_log(self) -> None:
        with open("event_log.txt", "w") as file:
            for event in self.event_log:
                file.write(event + "\n")

    def run(self) -> None:
        while True:
            # start loop and one turn at a time
            self.simulation()

            if (
                (len(self.zone_stat[self.graph.end_hub])
                 == len(self.drones_stat))):
                self.save_event_log()
                break

            time.sleep(1)

    def reset(self) -> None:
        self._initialize()

    def abs_distance(self, x: int, y: int) -> float:
        return (
            math.sqrt(
                (x - self.graph.start_hub.coordinates[0])**2 +
                (y - self.graph.start_hub.coordinates[1])**2
            ))
