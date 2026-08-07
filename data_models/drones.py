#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   drones.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/06 20:33:02 by jay-k               #+#    #+#            #
#   Updated: 2026/08/07 14:14:33 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from data_models.zone import Zone
# from data_models.connection import Connection


class Drone:
    def __init__(
        self, current_zone: Zone,
        came_from: list[Zone],
        zone_path: list[Zone]
    ) -> None:

        self.current_zone = current_zone
        self.zone_path = zone_path
        self.came_from = came_from

    # def __str__(self) -> str:
    #     return (
    #         f"Graph: {nb_zones} zones"
    #         f" and {nb_connections} connections\n\n"
    #         f"Start zone: {self.start_hub}\n"
    #         f"end zone: {self.end_hub}\n"
    #         f"Total drones: {self.total_drones}\n"
    #     )
