#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   zone.py                                              :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/04 13:13:14 by jay-k               #+#    #+#            #
#   Updated: 2026/08/06 12:53:14 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import sys


class Zone:
    ZONE_COSTS = {
        "normal": 1,
        "blocked": sys.maxsize,
        "restricted": 2,
        "priority": 1
    }

    def __init__(
        self, name: str,
        coordinates: tuple[int, int],
        type: str = "normal",
        color: str | None = None,
        max_drones: int = 1
    ) -> None:

        self.name = name
        self.coordinates = coordinates
        self.type = type
        self.color = color
        self.max_drones = max_drones

    def __str__(self) -> str:
        return (
            f"name: {self.name}\ncoordinates: {self.coordinates}\n"
            f"type: {self.type}\ncolor: {self.color}\n"
            f"maximum occupancy: {self.max_drones}\n"
        )
