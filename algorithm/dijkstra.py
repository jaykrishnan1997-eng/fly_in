#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   dijkstra.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jay-k <jay-k@student.42.fr>                  +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/06 10:55:37 by jkrishna            #+#    #+#            #
#   Updated: 2026/08/13 20:44:02 by jay-k              ###   ########.fr      #
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
    current_zone: Zone, blocked: list[Zone], connection: list[Connection]
) -> list[Zone]:
    neighbor: list[Zone] = []
    for line in connection:
        if (
            current_zone == line.zone_a
            and line.zone_b not in blocked
        ):
            neighbor.append(line.zone_b)
        elif (
            current_zone == line.zone_b
            and line.zone_a not in blocked
        ):
            neighbor.append(line.zone_a)
    return neighbor


def dijkstra(
    drone: Drone, blocked: list[Zone], graph: Graph
) -> list[Zone]:
    # must include restricted zone when the zone
    # is fully occupied in current, next and next-next move.
    current_zone: Zone = drone.current_zone
    start_zone: Zone = current_zone
    visited: Deque[Zone] = deque()
    cost_stat: dict[
        Zone, tuple[float, Zone | None]
    ] = {}
    for zone in graph.zones:
        if zone == current_zone:
            cost_stat.update({current_zone: (0, None)})
        else:
            cost_stat.update({zone: (sys.maxsize, None)})
    heap: list[tuple[float, int, Zone]] = []
    counter = 0
    heapq.heappush(heap, (0, counter, current_zone))
    while heap:
        current_zone = heapq.heappop(heap)[2]
        if current_zone not in visited:
            neighbors: list[Zone] = neighbor(
                current_zone, blocked, graph.connections)
            for zone in neighbors:
                total_cost = cost_stat[current_zone][0] + zone.cost
                if total_cost < cost_stat[zone][0]:
                    cost_stat[zone] = (total_cost, current_zone)
                    counter += 1
                    heapq.heappush(heap, (total_cost, counter,  zone))
            visited.append(current_zone)
        if current_zone == graph.end_hub:
            break
    heap.clear()
    path: list[Zone] = []
    while current_zone != start_zone:
        path.append(current_zone)
        previous = cost_stat[current_zone][1]
        if previous is None:
            break
        current_zone = previous
    path.append(start_zone)
    path.reverse()
    return path
