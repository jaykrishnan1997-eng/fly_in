#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   visual_generator.py                                  :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/15 13:00:33 by jkrishna            #+#    #+#            #
#   Updated: 2026/08/17 11:31:42 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

# from datetime import datetime

# from rich import box
# from rich.align import Align
# from rich.console import Console, Group
# from rich.layout import Layout
# from rich.panel import Panel
# from rich.table import Table
# from rich.text import text
# from rich.live import Live
# from data_models.graph import Graph
# from data_models.zone import Zone

# console = Console()

# # ┌──────────────────────────────────────────────────────────────┐
# # │ HEADER                                                       │
# # ├──────────────────────────────────┬───────────────────────────┤
# # │                                  │ SUMMARY                   │
# # │                                  |                           |
# # │           AIRSPACE MAP           |───────────────────────────│
# # │                                  │ LEGEND                    │
# # │                                  │                           │
# # ├──────────────────────────────────┴───────────────────────────┤
# # │ DRONES                           │ EVENT LOG                 │
# # ├──────────────────────────────────┴───────────────────────────┤
# # │ FOOTER / CONTROLS                                            │
# # └──────────────────────────────────────────────────────────────┘

# class Dashboard:
#     def __init__(
#         self,
#         graph: Graph,
#         zone_stat: dict[Zone, list[Drone]],
#         drones_stat: dict[Drone, deque[Zone]],
#         connection_stat: dict[Connection, list[Drone]],
#         zone_occupancy: dict[Zone, int],
#         connection_capacity: dict[Connection, int],
#     ) -> None:

#         self.graph = graph
#         self.zone_stat: dict[Zone, list[Drone]] = {}
#         self.drones_stat: dict[Drone, deque[Zone]] = {}
#         self.connection_stat: dict[Connection, list[Drone]] = {}
#         self.zone_occupancy: dict[Zone, int] = {}
#         self.connection_capacity: dict[Connection, int] = {}


#     def make_layout(self) -> Layout:
#         """Define the layout."""
#         layout = Layout(name="root")

#         layout.split(
#             Layout(name="header", size=3),
#             Layout(name="main", size=1),
#             Layout(name="footer", size=3),
#         )
#         layout["main"].split(
#             Layout(name="top", ratio=2),
#             Layout(name="bottom", ratio=1),
#         )
#         layout["top"].split(
#             Layout(name="map", ratio=2),
#             Layout(name="right", ratio=1),
#         )
#         layout["right"].split(
#             Layout(name="summary", ratio=1),
#             Layout(name="legend", ratio=1),
#         )
#         layout["bottom"].split(
#             Layout(name="drones", ratio=2),
#             Layout(name="events", ratio=1),
#         )
#
#         return layout
#
#
#     def make_header(self) -> Panel:
#         grid = Table.grid(expand=True)
#         grid.add_column(justify="left")
#         grid.add_column(justify="center", ratio=1)
#         grid.add_column(justify="right")
#         grid.add_row(
#             "FlyIn - Drone Traffic Simulation",
#             f"[bold green][ RUNNING ][/bold green]   Tick: {simulation.tick}"
#             f"Map: {map_name}",
#         )
#         return Panel(grid)
#
#
#     def make_summary(self) -> Panel:
#         table = Table.grid()
#
#         table.add_row(
#             "Total Drones",
#             str(self.graph.nb_drones),
#         )
#         table.add_row(
#             "Drones In Connections",
#             str(len()),
#         )
#         table.add_row(
#             "Drones In Zones",
#             str(len(simulation.drones)),
#         )
#         table.add_row(
#             "Completed Drones",
#             str(len(simulation.drones)),
#         )
#         table.add_row(
#             "Total Ticks",
#             str(len(simulation.drones)),
#         )
#         table.add_row(
#             "Average Transit Time",
#             str(len(simulation.drones)),
#         )
#
#
#
#     def make_legend(self) -> Panel:
#         pass

#     def make_drones_table() -> Panel:
#         pass

#     def make_event_log() -> Panel:
#         pass

#     def make_footer() -> Panel:
#         pass

#     # The core visual(the drones transit itself)
#     def make_map() -> Panel:
#         pass


# # with Live(layout, refresh_per_second=10, screen=True):
# #     while simulation_running:
# #         simulation.step()

#     def update(self):
#         self.layout["header"].update(make_header(simulation))
#         self.layout["header"].update(make_header(simulation))
#         self.layout["header"].update(make_header(simulation))
#         self.layout["header"].update(make_header(simulation))
#         self.layout["header"].update(make_header(simulation))
