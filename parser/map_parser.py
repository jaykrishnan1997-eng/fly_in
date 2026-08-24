#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   map_parser.py                                        :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/03 14:51:56 by jkrishna            #+#    #+#            #
#   Updated: 2026/08/24 13:53:57 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import re
from data_models.connection import Connection
from data_models.graph import Graph
from data_models.zone import Zone
import sys


class Parser:
    """ For parsing map information into graph object"""
    def __init__(self, path: str) -> None:
        self.path = path
        try:
            with open(path) as f:
                self.map = f.readlines()
        except OSError as e:
            print(f"Error opening file '{self.path}': {e}")
            sys.exit(1)

    def parser(self) -> Graph:
        nb_drones: int | None = None
        zones: list[Zone] = []
        connections: list[Connection] = []
        start_hub: Zone | None = None
        end_hub: Zone | None = None
        token: list[str] = []
        for line in self.map:
            line = line.split("#", 1)[0].strip()
            if not line:
                continue

            metadata = ""

            metadata_match = re.search(r"\[(.*?)\]", line)
            if metadata_match:
                metadata = metadata_match.group(1)
                line = re.sub(r"\[(.*?)\]", "", line).strip()

            token = line.split()

            if "nb_drones:" == token[0].lower():
                if len(token) != 2:
                    raise ValueError("Invalid nb_drones line")
                try:
                    nb_drones = int(token[1])
                except ValueError:
                    raise ValueError(f"Invalid nb_drones value on line {line}")
                if nb_drones < 1:
                    raise ValueError(
                        f"nb_drones must be posititve integer, got {nb_drones}"
                        f" on line: {line}"
                    )

            if token[0].lower() in {"hub:", "start_hub:", "end_hub:"}:

                if nb_drones is None:
                    raise ValueError("nb_drones must be defined before hubs")
                if len(token) < 4:
                    raise ValueError("Invalid hub definition")

                unit_type = "normal"
                unit_color = None
                unit_max_drones = 1

                try:
                    x = int(token[2])
                    y = int(token[3])
                except ValueError as e:
                    raise ValueError(f"Invalid coordinate info: {e}")
                for unit in metadata.split():
                    if "zone=" in unit:
                        unit_type = unit.split("=", 1)[1]
                        valid_zones = [
                            "normal", "blocked", "restricted", "priority"]
                        if unit_type.lower() not in valid_zones:
                            raise ValueError(
                                f"Invlaid zone_type '{unit_type}' "
                                f"on line: {line} - must be "
                                f"one of {valid_zones}"
                            )
                    elif "color=" in unit:
                        unit_color = unit.split("=", 1)[1]
                    elif "max_drones=" in unit:
                        try:
                            unit_max_drones = int(unit.split("=", 1)[1])
                        except ValueError:
                            raise ValueError(
                                f"Invalid max_drones value on line: {line}"
                            )
                        if unit_max_drones < 1:
                            raise ValueError(
                                f"Invalid max_drones value '{unit_max_drones}'"
                                f"on line: {line} - "
                                "must be a positive integer"
                            )

                if token[0].lower() == "start_hub:":
                    start_hub = Zone(
                        token[1],
                        (x, y),
                        unit_type,
                        unit_color,
                        nb_drones
                    )
                    if start_hub in zones:
                        raise ValueError(
                            "multiple copies of a start_hub detected")
                    zones.append(start_hub)
                elif token[0].lower() == "end_hub:":
                    end_hub = Zone(
                        token[1],
                        (x, y),
                        unit_type,
                        unit_color,
                        nb_drones
                    )
                    if end_hub in zones:
                        raise ValueError(
                            "multiple copies of a end_hub detected")
                    zones.append(end_hub)
                else:
                    new_zone = Zone(
                        token[1],
                        (x, y),
                        unit_type,
                        unit_color,
                        unit_max_drones
                    )
                    if new_zone in zones:
                        raise ValueError("multiple copies of a hub detected")
                    zones.append(new_zone)

            if token[0].lower() == "connection:":
                max_link_capacity: int = 1

                if len(token) < 2:
                    raise ValueError("Invalid connection definition")

                connection_data = token[1]
                zone_data = connection_data.split("-")

                if len(zone_data) != 2:
                    raise ValueError("Invalid connection format")

                if zone_data[0] == zone_data[1]:
                    raise ValueError("A zone cannot be connected to itself")

                zone_a: Zone | None = None
                zone_b: Zone | None = None

                for zone in zones:
                    if zone.name == zone_data[0]:
                        zone_a = zone
                    if zone.name == zone_data[1]:
                        zone_b = zone

                if zone_a is None or zone_b is None:
                    raise ValueError("Unknown Zone data received")

                for unit in metadata.split():
                    if "max_link_capacity=" in unit:
                        try:
                            max_link_capacity = int(unit.split("=", 1)[1])
                        except ValueError:
                            raise ValueError(
                                "Invalid max_link_capacity"
                                f"value on line: {line}"
                            )
                        if max_link_capacity < 1:
                            raise ValueError(
                                "Invalid max_link_capacity "
                                f"value '{max_link_capacity}' "
                                f"on line: {line} - must be a "
                                "positive integer"
                            )
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
                    raise ValueError("Duplicate connections detected!")
                connections.append(new_connection)

        if start_hub is None or end_hub is None:
            raise ValueError("Missing start_hub or end_hub")

        if nb_drones is None:
            raise ValueError("Missing nb_drones")

        zones = sorted(zones, key=lambda z: z.coordinates)
        try:
            graph_object: Graph = Graph(
                self.path,
                zones,
                connections,
                start_hub,
                end_hub,
                nb_drones
            )
        except Exception as e:
            raise ValueError(f"Error creating graph: {e}")
        return graph_object
