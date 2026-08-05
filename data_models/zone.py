#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   zone.py                                              :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/04 13:13:14 by jay-k               #+#    #+#            #
#   Updated: 2026/08/05 11:02:18 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

class Zone:
    def __init__(
        self, name: str,
        x: int, y: int,
        type: str = "normal",
        color: str | None = None,
        max_drones: int = 1
    ) -> None:

        self.name = name
        self.x = x
        self.y = y
        self.type = type
        self.color = color
        self.max_drones = max_drones

    def __str__(self) -> str:
        return (
            f"name: {self.name}\ncoordinates: ({self.x}, {self.y})\n"
            f"type: {self.type}\ncolor: {self.color}"
            f"maximum occupancy: {self.max_drones}"
        )
