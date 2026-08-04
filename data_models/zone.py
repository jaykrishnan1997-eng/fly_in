#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   zone.py                                              :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jay-k <jay-k@student.42.fr>                  +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/04 13:13:14 by jay-k               #+#    #+#            #
#   Updated: 2026/08/04 19:18:24 by jay-k              ###   ########.fr      #
#                                                                             #
# ########################################################################### #

class Zone:
    def __init__(
        self, name: str,
        x: int, y: int,
        type: str, color: str | None = None,
        max_occupancy: int = 1
    ) -> None:

        self.name = name
        self.x = x
        self.y = y
        self.type = type
        self.color = color
        self.max_occupancy = max_occupancy

    def __str__(self) -> str:
        return (
            f"name: {self.name}\ncoordinates: ({self.x}, {self.y})\n"
            f"type: {self.type}\ncolor: {self.color}"
            f"maximum occupancy: {self.max_occupancy}"
        )
