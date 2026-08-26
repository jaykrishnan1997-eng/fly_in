#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   graph.py                                             :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jay-k <jay-k@student.42.fr>                  +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/04 19:46:41 by jay-k               #+#    #+#            #
#   Updated: 2026/08/26 13:22:37 by jay-k              ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from data_models.zone import Zone
from data_models.connection import Connection


class Graph:
    def __init__(
        self,
        map: str,
        zones: list[Zone],
        connections: list[Connection],
        start_hub: Zone,
        end_hub: Zone,
        total_drones: int
    ) -> None:

        self.map = map
        self.zones = zones
        self.connections = connections
        self.start_hub = start_hub
        self.end_hub = end_hub
        self.total_drones = total_drones

    def get_connection(self, z_a: Zone, z_b: Zone) -> Connection | None:
        for connection in self.connections:
            if (
                (connection.zone_a == z_a and connection.zone_b == z_b)
                or
                (connection.zone_a == z_b and connection.zone_b == z_a)
            ):
                return connection
        return None

    # def __str__(self) -> str:
    #     nb_zones = len(self.zones)
    #     nb_connections = len(self.connections)
    #     return (
    #         f"Graph: {nb_zones} zones"
    #         f" and {nb_connections} connections\n\n"
    #         f"Start zone: {self.start_hub}\n"
    #         f"end zone: {self.end_hub}\n"
    #         f"Total drones: {self.total_drones}\n"
    #     )
