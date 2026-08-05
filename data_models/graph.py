#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   graph.py                                             :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/04 19:46:41 by jay-k               #+#    #+#            #
#   Updated: 2026/08/05 11:03:45 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from data_models.zone import Zone
from data_models.connection import Connection


class Graph:
    def __init__(
        self, zones: list[Zone],
        connections: list[Connection],
        start_hub: Zone,
        end_hub: Zone,
        total_drones: int
    ) -> None:

        self.zones = zones
        self.connections = connections
        self.start_hub = start_hub
        self.end_hub = end_hub
        self.total_drones = total_drones

    def __str__(self) -> str:
        return (
            f"Graph: len({self.zones} zones"
            f" and len({self.connections} connections)\n"
            f"Start zone: {self.start_hub}\n"
            f"end zone: {self.end_hub}\n"
            f"Total drones: {self.total_drones}"
        )
