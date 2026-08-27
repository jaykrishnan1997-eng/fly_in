#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   drones.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jay-k <jay-k@student.42.fr>                  +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/06 20:33:02 by jay-k               #+#    #+#            #
#   Updated: 2026/08/27 23:35:59 by jay-k              ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from data_models.zone import Zone
from data_models.connection import Connection


class Drone:
    """Represent a drone and its current simulation state."""
    def __init__(
        self, current_zone: Zone,
        came_from: list[Zone],
        drone_id: int
    ) -> None:
        """Initialize a drone.

        Args:
            current_zone: Zone where the drone currently is.
            came_from: Zones previously visited by the drone.
            drone_id: Unique identifier of the drone.
        """
        self.id = drone_id
        self.current_zone: Zone = current_zone
        self.came_from = came_from

        # transit state
        self.current_connection: Connection | None = None
        self.destination: Zone | None = None
        self.turns_remaining = 0

        # visualization
        self.previous_zone: Zone | None = None
        self.visual_destination: Zone | None = None
        self.visual_progress: float = 0.0

    def start_transit(
        self, connection: Connection,
        destination: Zone
    ) -> None:
        """Start moving the drone through a connection.

        Args:
            connection: Connection the drone is entering.
            destination: Zone where the drone will arrive.
        """
        self.current_connection = connection
        self.destination = destination
        self.turns_remaining = destination.cost - 1

        if destination.cost > 1:
            self.visual_progress = 0.5
        else:
            self.visual_progress = 0.0

    def update_transit(self) -> None:
        """Advance the drone by one turn while in transit.

        The drone reaches its destination when no turns remain.
        """
        self.turns_remaining -= 1

        if self.turns_remaining <= 0:
            if self.destination is not None:
                self.current_zone = self.destination

                # Visual map is now complete
                self.previous_zone = self.current_zone
                self.visual_destination = None
                self.visual_progress = 0.0

            self.current_connection = None
            self.destination = None
            self.turns_remaining = 0
