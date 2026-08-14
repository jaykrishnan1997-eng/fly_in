#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   drones.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/06 20:33:02 by jay-k               #+#    #+#            #
#   Updated: 2026/08/14 15:11:01 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from data_models.zone import Zone
from data_models.connection import Connection


class Drone:
    def __init__(
        self, current_zone: Zone,
        came_from: list[Zone],
        drone_id: int
    ) -> None:

        self.id = drone_id
        self.current_zone: Zone = current_zone
        # self.zone_path = zone_path
        self.came_from = came_from

        # transit state
        self.current_connection: Connection | None = None
        self.destination: Zone | None = None
        self.turns_remaining = 0

    def start_transit(
        self, connection: Connection,
        destination: Zone
    ) -> None:
        self.current_connection = connection
        self.destination = destination
        self.turns_remaining = destination.cost - 1

    def update_transit(self) -> None:
        self.turns_remaining -= 1

        if self.turns_remaining == 0:
            if self.destination is not None:
                self.current_zone = self.destination

            self.current_connection = None
            self.destination = None

    # def __str__(self) -> str:
    #     return (
    #         f"Graph: {nb_zones} zones"
    #         f" and {nb_connections} connections\n\n"
    #         f"Start zone: {self.start_hub}\n"
    #         f"end zone: {self.end_hub}\n"
    #         f"Total drones: {self.total_drones}\n"
    #     )
