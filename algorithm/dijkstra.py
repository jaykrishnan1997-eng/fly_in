#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   dijkstra.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/06 10:55:37 by jkrishna            #+#    #+#            #
#   Updated: 2026/08/06 15:15:10 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

# import heapq
# from data_models.graph import Graph
# from data_models.connection import Connection
# from data_models.zone import Zone
# from typing import Callable


# def solver(self, graph: Graph) -> None:
#     cost_dictionary: dict[Connection: Callable,
#  list[int, int]] = cost(graph.zones, graph.connections)
#     dijkstra()

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


# def dijkstra(graph: Graph) -> dict[str:dict]:
#     data: dict[Zone, int, Zone] = {}
#     pass
# # h = []
# # heapq.heappush(h, 1)
# # heapq.heappush(h, 2)
# # print([heapq.heappop(h) for _ in range(2)])
