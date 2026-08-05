#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   map_parser.py                                        :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/03 14:51:56 by jkrishna            #+#    #+#            #
#   Updated: 2026/08/05 15:13:02 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

# import re
from data_models.connection import Connection
from data_models.graph import Graph
from data_models.zone import Zone
# from typing import List
import sys


class zone_types():
    {
        "normal": 1,
        "blocked": sys.maxsize,
        "restricted": 2,
        "priority": 1
    }


class Parser():
    """ For parsing map information into graph object"""
    def __init__(self, path: str) -> None:
        self.path = path
        try:
            with open(path) as f:
                self.map = f
        except Exception as e:
            print(f"Error opening file '{path}': {e}")
            sys.exit(1)

    def parser(self) -> Graph:
        nb_drones: int
        zones: list[Zone] = []
        connections: list[Connection] = []
        start_hub: Zone
        end_hub: Zone
        token: list[str] = []
        for line in self.map:
            token = line.split()

            if "nb_drones:" == token[0].lower():
                nb_drones = int(token[1])

            if "hub:" in token[0].lower():
                unit_type = "normal"
                unit_color = None
                unit_max_drones = 1
                for element in token:
                    if "[" in element and "]" in element:
                        metadata1: list[str] = (
                            (element.strip("[")).strip("]")
                        ).split()
                        for unit in metadata1:
                            if "zone=" in unit:
                                unit_type = unit.strip("zone=")
                            if "color=" in unit:
                                unit_color = unit.strip("color=")
                            if "max_drones=" in unit:
                                unit_max_drones = int(
                                    unit.strip("max_drones=")
                                )
                if "start_hub:" == token[0].lower():
                    start_hub = Zone(
                        token[1],
                        (int(token[2]), int(token[3])),
                        unit_type,
                        unit_color,
                        nb_drones
                    )
                    if start_hub in zones:
                        raise ValueError("multiple copies of a zone detected")
                        sys.exit(1)
                elif "end_hub:" == token[0].lower():
                    end_hub = Zone(
                        token[1],
                        (int(token[2]), int(token[3])),
                        unit_type,
                        unit_color,
                        nb_drones
                    )
                    if start_hub in zones:
                        raise ValueError("multiple copies of a zone detected")
                        sys.exit(1)
                else:
                    new_zone = Zone(
                            token[1],
                            (int(token[2]), int(token[3])),
                            unit_type,
                            unit_color,
                            unit_max_drones
                    )
                    if new_zone in zones:
                        raise ValueError("multiple copies of a zone detected")
                        sys.exit(1)
                    zones.append(new_zone)

            zones = sorted(zones, key=lambda z: z.coordinates)

            if "connection" == token[0].lower():
                max_link_capacity: int = 1
                for element in token:
                    if "[" in element and "]" in element:
                        metadata2: str = (element.strip("[")).strip("]")
                        if "max_link_capacity=" in metadata2:
                            max_link_capacity = int(metadata2.strip(
                                "max_link_capacity="
                            ))
                    if "-" in element and element == token[1]:
                        zone_data: list[str] = element.split("-")
                        try:
                            for zone in zones:
                                if zone.name == zone_data[0]:
                                    zone_a: Zone = zone
                                elif zone.name == zone_data[1]:
                                    zone_b: Zone = zone
                                else:
                                    raise ValueError
                        except Exception as e:
                            print(f" Unknown Zone data recieved:{e}")
                            sys.exit(1)
                    new_connection = Connection(
                        zone_a, zone_b,
                        max_link_capacity
                    )
                    rev_connection = Connection(
                        zone_b, zone_a,
                        max_link_capacity
                    )
                    if (
                        new_connection in connections
                        or rev_connection in connections
                    ):
                        print("Duplicate connections detected!")
                        sys.exit(1)
                connections.append(new_connection)
        try:
            graph_object: Graph = Graph(
                zones, connections, start_hub, end_hub, nb_drones
            )
        except Exception as e:
            print(f"Error detected: {e}")
        return graph_object

# """ parse_zone:
#         Parses a zone definition line and extracts metadata.
#         Its only job is to convert a list of words into a Zone object.

#         Args:
#             tokens: A list of strings representing the split line
#             from the file.

#         Returns:
#             A Zone object populated with the parsed data.

#         Raises:
#             ValueError: If an invalid zone type is encountered.
#         """parse:
#         """Reads a file and constructs the Graph
#             representing the drone network.

#         Args:
#             filepath: Path to the input map file.

#         Returns:
#             A fully initialized Graph object.

#         Raises:
#             ValueError: If parsing fails due to syntax errors, missing hubs,
#                 duplicate c, or invalid drone counts.
#             FileNotFoundError: If the specified file does not exist.
#         """
#         """parse_pos_int:Parses and validates a positive integer
# within MAX_VALUE."""
#         """register_zone:Registers a zone and checks for duplicates."""
