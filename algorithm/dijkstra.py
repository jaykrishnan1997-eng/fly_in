#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   dijkstra.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jay-k <jay-k@student.42.fr>                  +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/06 10:55:37 by jkrishna            #+#    #+#            #
#   Updated: 2026/08/27 18:02:58 by jay-k              ###   ########.fr      #
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
    current_zone: Zone, blocked: list[Zone], connection: list[Connection],
    excluded_connection: Connection | None = None
) -> list[Zone]:
    """Return neighboring zones reachable from the current zone.

    Args:
        current_zone: Zone from which to find neighbors.
        blocked: Zones that cannot be entered.
        connection: Connections available in the graph.
        excluded_connection: Optional connection to ignore.

    Returns:
        A list of reachable neighboring zones.
    """
    neighbor: list[Zone] = []
    for line in connection:
        if line == excluded_connection:
            continue
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
    drone: Drone, blocked: list[Zone], graph: Graph,
    excluded_connection: Connection | None = None
) -> list[Zone]:
    """Find the cheapest path from a drone to the end hub.

    Args:
        drone: Drone for which the path is calculated.
        blocked: Zones that cannot be used in the path.
        graph: Graph containing zones and connections.
        excluded_connection: Optional connection to avoid.

    Returns:
        A list of zones forming the path from the drone to the end hub.
        Returns only the current zone if the end hub is unreachable.
    """
    current_zone: Zone = drone.current_zone
    start_zone: Zone = current_zone
    visited: Deque[Zone] = deque()

    # Zone -> (cheapest known cost, previous zone)
    cost_stat: dict[
        Zone, tuple[float, Zone | None]
    ] = {}

    # Initialize S with 0 and None and remaining all 
    # inf and None
    for zone in graph.zones:
        if zone == current_zone:
            cost_stat.update({current_zone: (0, None)})
        else:
            cost_stat.update({zone: (sys.maxsize, None)})

    # (cost, priority_nbr, counter, zone)
    # Python's heap compares tuples from left to right
    heap: list[tuple[float, int, int, Zone]] = []
    counter = 0
    heapq.heappush(heap, (0, current_zone.priority_nbr, counter, current_zone))

    while heap:
        current_zone = heapq.heappop(heap)[3]
        if current_zone not in visited:
            neighbors: list[Zone] = neighbor(
                current_zone, blocked, graph.connections, excluded_connection)
            for zone in neighbors:
                total_cost = cost_stat[current_zone][0] + zone.cost
                if total_cost < cost_stat[zone][0]:
                    cost_stat[zone] = (total_cost, current_zone)
                    counter += 1
                    heapq.heappush(heap, (
                        total_cost, zone.priority_nbr, counter,  zone))
            visited.append(current_zone)
        if current_zone == graph.end_hub:
            break
    heap.clear()

    if cost_stat[graph.end_hub][0] == sys.maxsize:
        return [start_zone]

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
