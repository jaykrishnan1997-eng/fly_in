#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   visual_generator.py                                  :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/15 13:00:33 by jkrishna            #+#    #+#            #
#   Updated: 2026/08/17 14:29:22 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

# # from datetime import datetime

# # from rich import box
# # from rich.align import Align
# from rich.console import Console
# # from rich.console import Group
# from rich.layout import Layout
# from rich.panel import Panel
# from rich.table import Table
# # from rich.text import text
# # from rich.live import Live
# from data_models.graph import Graph
# from data_models.zone import Zone
# from data_models.drone import Drone
# from data_models.connection import Connection
# from collections import deque

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
#         ticks: int,
#         total_turns: int,
#         zone_stat: dict[Zone, list[Drone]],
#         drones_stat: dict[Drone, deque[Zone]],
#         connection_stat: dict[Connection, list[Drone]],
#         zone_occupancy: dict[Zone, int],
#         connection_capacity: dict[Connection, int],
#         waiting: list[Drone],
#     ) -> None:

#         self.graph = graph
#         self.ticks = ticks
#         self.total_turns = total_turns
#         self.zone_stat = zone_stat
#         self.drones_stat = drones_stat
#         self.connection_stat = connection_stat
#         self.zone_occupancy = zone_occupancy
#         self.connection_capacity = connection_capacity
#         self.waiting = waiting

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

#         return layout

#     def make_header(self) -> Panel:
#         grid = Table.grid(expand=True)
#         grid.add_column(justify="left")
#         grid.add_column(justify="center", ratio=1)
#         grid.add_column(justify="right")
#         grid.add_row(
#             "FlyIn - Drone Traffic Simulation",
#             f"[bold green][ RUNNING ][/bold green]   Tick: {self.ticks}"
#             f"Map: {map_name}",
#         )
#         return Panel(grid)

#     def make_summary(self) -> Panel:
#         table = Table.grid()

#         table.add_row(
#             "Total Drones",
#             str(self.graph.nb_drones),
#         )
#         table.add_row(
#             "Drones In Connections",
#             str(sum(self.connection_stat.values())),
#         )
#         nb_transit_drones = 0
#         for zone in self.zone_stat.keys():
#             if zone not in (self.graph.start_hub, self.graph.end_hub):
#                 nb_transit_drones += len(self.zone_stat[zone])
#         table.add_row(
#             "Drones In Transit Zones",
#             str(nb_transit_drones),
#         )
#         table.add_row(
#             "Completed Drones",
#             str(self.zone_occupancy[self.graph.end_hub]),
#         )
#         table.add_row(
#             "Total Ticks",
#             str(self.ticks),
#         )
#         table.add_row(
#             "Total turns",
#             str(self.total_turns),
#         )

#     # is a legend actually necessary in my case. Since evry
#     # zone has its own colours and so on.
#     # def make_legend(self) -> Panel:
#     #     table = Table.grid()
#     #
#     #     table.add_row(
#     #         "Total Drones",
#     #         str(self.graph.nb_drones),
#     #     )
#     #     table.add_row(
#     #         "Drones In Connections",
#     #         str(sum(self.connection_stat.values())),
#     #     )
#     #     nb_transit_drones = 0
#     #     for zone in self.zone_stat.keys():
#     #         if zone not in (self.graph.start_hub, self.graph.end_hub):
#     #             nb_transit_drones += len(zone_stat[zone])
#     #     table.add_row(
#     #         "Drones In Transit Zones",
#     #         str(nb_transit_drones),
#     #     )
#     #     table.add_row(
#     #         "Completed Drones",
#     #         str(self.zone_occupancy[self.graph.end_hub]),
#     #     )
#     #     table.add_row(
#     #         "Total Ticks",
#     #         str(self.ticks),
#     #     )
#     #     table.add_row(
#     #         "Total turns",
#     #         str(self.total_turns),
#     #     )


#     def make_drones_table(self) -> Panel:
#         table = Table.grid(expand=True)

#         table.add_row(
#                 "DRONE ID",
#                 "CURRENT ZONE",
#                 "PATH (NEXT -> ...)",
#                 "STATUS",
#                 "WAITING",
#             )
#         for drone in self.drones_stat.keys():
#             drone_path = ""
#             status = ""
#             waiting_status = ""
#             length = len(self.drones_stat[drone])

#             if length == 1:
#                 drone_path = ""
#             else:
#                 for i in range(1, length):
#                     if i != length - 1:
#                         drone_path += f"{self.drones_stat[drone][i].id} -> "
#                     else:
#                         drone_path += str(self.drones_stat[drone][i].id)

#             if drone.current_zone == self.graph.end_hub:
#                 status = "IN_END_ZONE"
#             else:
#                 status = "IN_TRANSIT"

#             if drone in self.waiting:
#                 waiting_status = "YES"
#             else:
#                 waiting_status = "NO"
#             table.add_row(
#                 str(drone.id),
#                 str(drone.current_zone),
#                 drone_path,
#                 status,
#                 str(waiting_status),
#             )


#     def make_event_log(self) -> Panel:
#         pass

#     def make_footer(self) -> Panel:
#         pass

#     # The core visual(the drones transit itself)
#     def make_map(self) -> Panel:
#         pass


# # with Live(layout, refresh_per_second=10, screen=True):
# #     while simulation_running:
# #         simulation.step()

#     def update(self):
#         self.layout["header"].update(make_header())
