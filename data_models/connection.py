#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   connection.py                                        :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jay-k <jay-k@student.42.fr>                  +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/04 16:45:46 by jay-k               #+#    #+#            #
#   Updated: 2026/08/04 20:15:02 by jay-k              ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from data_models.zone import Zone


class Connection:
    def __init__(
        self, zone_a: Zone,
        zone_b: Zone,
        max_drones: int = 1
    ) -> None:

        self.zone_a = zone_a
        self.zone_b = zone_b
        self.max_drones = max_drones

    def __str__(self) -> str:
        return (
            f"Zone_a: {self.zone_a}\nZone_b: {self.zone_b}\n"
            f"maximum drones allowed: {self.max_drones}"
        )
