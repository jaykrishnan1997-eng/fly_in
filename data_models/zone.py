#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   zone.py                                              :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jay-k <jay-k@student.42.fr>                  +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/04 13:13:14 by jay-k               #+#    #+#            #
#   Updated: 2026/08/27 22:40:42 by jay-k              ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import sys


class Zone:
    """Represent a zone in the drone traffic map."""
    ZONE_COSTS = {
        "normal": (1, 1),
        "blocked": (sys.maxsize, 4),
        "restricted": (2, 3),
        "priority": (1, 0),
    }

    def __init__(
        self, name: str,
        coordinates: tuple[int, int],
        type: str = "normal",
        color: str | None = None,
        max_drones: int = 1
    ) -> None:
        """Initialize a zone with its properties and movement cost.

        Args:
            name: Name identifying the zone.
            coordinates: X and Y coordinates of the zone.
            type: Zone type determining its cost and priority.
            color: Optional color used by the visualizer.
            max_drones: Maximum number of drones allowed in the zone.
        """

        self.name = name
        self.coordinates = coordinates
        self.type = type
        self.color = color
        self.max_drones = max_drones
        self.cost = Zone.ZONE_COSTS[type][0]
        self.priority_nbr = Zone.ZONE_COSTS[type][1]

    # def __str__(self) -> str:
    #     return (
    #         f"name: {self.name}\ncoordinates: {self.coordinates}\n"
    #         f"type: {self.type}\ncolor: {self.color}\n"
    #         f"maximum occupancy: {self.max_drones}\n"
    #     )
