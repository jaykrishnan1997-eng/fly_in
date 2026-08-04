#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   graph.py                                             :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jay-k <jay-k@student.42.fr>                  +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/04 19:46:41 by jay-k               #+#    #+#            #
#   Updated: 2026/08/04 20:14:50 by jay-k              ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from data_models.zone import Zone
from data_models.connection import Connection


class Graph:
    def __init__(
        self, zones: list[Zone],
        connections: list[Connection],
        start: Zone,
        stop: Zone,
        total_drones: int
    ) -> None:

        self.zones = zones
        self.connections = connections
        self.start = start
        self.stop = stop
        self.total_drones = total_drones

    def __str__(self) -> str:
        return (
            f"Graph: len({self.zones} zones"
            f" and len({self.connections} connections)\n"
            f"Start zone: {self.start}\n"
            f"Stop zone: {self.stop}\n"
            f"Total drones: {self.total_drones}"
        )
