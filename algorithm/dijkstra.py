#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   dijkstra.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/06 10:55:37 by jkrishna            #+#    #+#            #
#   Updated: 2026/08/07 16:14:59 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import sys
import heapq
from data_models.graph import Graph
from data_models.connection import Connection
from data_models.zone import Zone
from data_models.drones import Drone
from collections import deque
from typing import Deque


def neighbor(
    current_zone: Zone, came_from: list[Zone], connection: list[Connection]
) -> list[Zone]:
    neighbor: list[Zone] = []
    for line in connection:
        if (
            current_zone == line.zone_a
            and line.zone_b not in came_from
        ):
            neighbor.append(line.zone_b)
        elif (
            current_zone == line.zone_b
            and line.zone_a not in came_from
        ):
            neighbor.append(line.zone_a)
    return neighbor


def dijkstra(
    drone: Drone, zone_stat: dict[Zone, int], graph: Graph
) -> list[Zone]:
    # must include restricted zone when the zone
    # is fully occupied in current, next and next-next move.
    current_zone: Zone = drone.current_zone
    visited: Deque[Zone] = deque()
    cost_stat: dict[
        Zone, tuple[float, Zone | None]
    ] = {}
    for zone in graph.zones:
        if zone == current_zone:
            cost_stat.update({current_zone: (0, None)})
        else:
            cost_stat.update({zone: (sys.maxsize, None)})
    heap: list[tuple[float, Zone]] = []
    heapq.heappush(heap, (0, current_zone))
    while heap:
        current_zone = heapq.heappop(heap)[1]
        if current_zone not in visited:
            neighbors: list[Zone] = neighbor(
                current_zone, drone.came_from, graph.connections)
            for zone in neighbors:
                total_cost = cost_stat[current_zone][0] + zone.cost
                if total_cost < cost_stat[zone][0]:
                    cost_stat[zone] = (total_cost, current_zone)
                    heapq.heappush(heap, (total_cost, zone))
            visited.append(current_zone)
        if current_zone == graph.end_hub:
            break
    heap.clear()
    path: list[Zone] = []
    while current_zone != graph.start_hub:
        path.append(current_zone)
        previous = cost_stat[current_zone][1]
        if previous is None:
            break
        current_zone = previous
    path.append(graph.start_hub)
    path.reverse()
    return path


# def cost(
#     zones: Zone, connection: Connection
# ) -> dict[Connection: Callable, list[int, int]]:
#     # cost is a dict with connection object,
#     # list with cost of end zone and max capacity of that particular line
#     cost_dictionary: dict[Connection, list[int, int]] = {}
#     for line in connection:
#         cost.append(
#             line,
#             [Zone.ZONE_COSTS[line.zone_b.type], line.max_link_capacity]
#         )
#     return cost_dictionary
# def solver(self, graph: Graph) -> None:
#     cost_dictionary: dict[Connection: Callable,
#  list[int, int]] = cost(graph.zones, graph.connections)
#     dijkstra()
# cost, prev_zone = cost_stat[zone]


# start = self._entry_coord
# end = self._exit_coord
# queue = deque([start])
# visited = {start}
# came_from: dict[tuple[int, int], tuple[tuple[int, int], str]] = {}

# while queue:
#     current = queue.popleft()
#     if current == end:
#         break
#     x, y = current
#     for dir, bit, (dx, dy) in DIRECTIONS:
#         # open wall check. if yes wall is open so walkable
#         if self._grid[y][x] & bit == 0:
#             neighbor = (x + dx, y + dy)
#             # skipping off grid (entry and exit doorway)
#             if not (
#                 0 <= neighbor[0] < self._width and
#                 0 <= neighbor[1] < self._height
#             ):
#                 continue
#             if neighbor not in visited:
#                 visited.add(neighbor)
#                 queue.append(neighbor)
#                 came_from[neighbor] = (current, dir)

# if end not in came_from and start != end:
#     raise ValueError(f"No path found between {start} and {end}")
# return came_from`
