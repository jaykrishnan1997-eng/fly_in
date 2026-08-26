#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   connection.py                                        :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jay-k <jay-k@student.42.fr>                  +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/04 16:45:46 by jay-k               #+#    #+#            #
#   Updated: 2026/08/26 13:22:33 by jay-k              ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from data_models.zone import Zone


class Connection:
    def __init__(
        self,
        zone_a: Zone,
        zone_b: Zone,
        max_link_capacity: int = 1
    ) -> None:

        self.name = f"{zone_a.name}-{zone_b.name}"
        self.zone_a = zone_a
        self.zone_b = zone_b
        self.max_link_capacity = max_link_capacity

    # def __str__(self) -> str:
    #     return (
    #         f"Zone_a: {self.zone_a}\nZone_b: {self.zone_b}\n"
    #         f"maximum drones allowed: {self.max_link_capacity}"
    #     )
