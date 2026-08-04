#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   map_parser.py                                        :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jay-k <jay-k@student.42.fr>                  +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/03 14:51:56 by jkrishna            #+#    #+#            #
#   Updated: 2026/08/04 22:38:46 by jay-k              ###   ########.fr      #
#                                                                             #
# ########################################################################### #

# import re
# from data_models.connection import Connection
# from data_models.graph import Graph
# from data_models.zone import Zone
# from typing import List

# class Parser():
#     """ For parsing map information into graph object"""
#     def parse_line(self, line: List[str]):
#         pass


#     def parse(self, path: str):
#         self.path = path
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
#                 duplicate connections, or invalid drone counts.
#             FileNotFoundError: If the specified file does not exist.
#         """
#         """parse_pos_int:Parses and validates a positive integer
# within MAX_VALUE."""
#         """register_zone:Registers a zone and checks for duplicates."""
