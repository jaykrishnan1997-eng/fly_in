#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   visual_generator.py                                  :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jay-k <jay-k@student.42.fr>                  +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/15 13:00:33 by jkrishna            #+#    #+#            #
#   Updated: 2026/08/17 21:16:05 by jay-k              ###   ########.fr      #
#                                                                             #
# ########################################################################### #

# from datetime import datetime
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from core.engine import Engine

# ┌──────────────────────────────────────────────────────────────┐
# │ HEADER                                                       │
# ├──────────────────────────────────┬───────────────────────────┤
# │                                  │ SUMMARY                   │
# │                                  |                           |
# │           AIRSPACE MAP           |───────────────────────────│
# │                                  │ LEGEND                    │
# │                                  │                           │
# ├──────────────────────────────────┴───────────────────────────┤
# │ DRONES                           │ EVENT LOG                 │
# ├──────────────────────────────────┴───────────────────────────┤
# │ FOOTER / CONTROLS                                            │
# └──────────────────────────────────────────────────────────────┘


class Dashboard:
    def __init__(self, engine: Engine) -> None:

        self.engine = engine
        self.layout = self.make_layout()

    def make_layout(self) -> Layout:
        """Define the layout."""
        layout = Layout(name="root")

        layout.split(
            Layout(name="header", size=3),
            Layout(name="main", size=1),
            Layout(name="footer", size=3),
        )
        layout["main"].split(
            Layout(name="top", ratio=2),
            Layout(name="bottom", ratio=1),
        )
        layout["top"].split(
            Layout(name="map", ratio=2),
            Layout(name="right", ratio=1),
        )
        layout["right"].split(
            Layout(name="summary", ratio=1),
        )
        layout["bottom"].split(
            Layout(name="drones", ratio=2),
            Layout(name="events", ratio=1),
        )

        return layout

    def make_header(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="left")
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            "FlyIn - Drone Traffic Simulation",
            "[bold green][ RUNNING ][/bold green]   "
            f"Tick: {self.engine.ticks}    |   Map: {self.engine.graph.map}"
        )
        return Panel(grid)

    def make_summary(self) -> Panel:
        table = Table.grid()

        table.add_row(
            "Total Drones",
            str(self.engine.graph.total_drones),
        )
        table.add_row(
            "Drones In Connections",
            str(sum(
                len(drones)
                for drones in self.engine.connection_stat.values())),
        )
        nb_transit_drones = 0
        for zone in self.engine.zone_stat.keys():
            if zone not in (
                self.engine.graph.start_hub,
                self.engine.graph.end_hub
            ):
                nb_transit_drones += len(self.engine.zone_stat[zone])
        table.add_row(
            "Drones In Transit Zones",
            str(nb_transit_drones),
        )
        table.add_row(
            "Completed Drones",
            str(self.engine.zone_occupancy[self.engine.graph.end_hub]),
        )
        table.add_row(
            "Total Ticks",
            str(self.engine.ticks),
        )
        table.add_row(
            "Total turns",
            str(self.engine.total_turns),
        )
        return Panel(table, title="Simulation Summary")

    def make_drones_table(self) -> Panel:
        table = Table(expand=True)

        table.add_column("DRONE ID")
        table.add_column("CURRENT ZONE")
        table.add_column("PATH (NEXT -> ...)")
        table.add_column("STATUS")
        table.add_column("WAITING")

        for drone in self.engine.drones_stat.keys():
            drone_path = ""
            status = ""
            waiting_status = ""
            length = len(self.engine.drones_stat[drone])

            if length == 1:
                drone_path = ""
            else:
                for i in range(1, length):
                    if i != length - 1:
                        drone_path += f"{
                            self.engine.drones_stat[drone][i].name} -> "
                    else:
                        drone_path += str(
                            self.engine.drones_stat[drone][i].name)

            if drone.current_zone == self.engine.graph.end_hub:
                status = "IN_END_ZONE"
            else:
                status = "IN_TRANSIT"

            if drone in self.engine.waiting:
                waiting_status = "YES"
            else:
                waiting_status = "NO"
            table.add_row(
                str(drone.id),
                str(drone.current_zone),
                drone_path,
                status,
                str(waiting_status),
            )
        return Panel(table, title="Drones")

    def make_event_log(self) -> Panel:
        table = Table.grid(expand=True)

        visible_events = self.engine.event_log[-8:]

        for event in visible_events:
            table.add_row(event)

        return Panel(table, title="Event Log")

    def make_footer(self) -> Panel:
        return Panel("Controls")

    # The core visual(the drones transit itself)
    def make_map(self) -> Panel:
        return Panel("Airspace Map")
# with Live(layout, refresh_per_second=10, screen=True):
#     while simulation_running:
#         simulation.step()

    def update(self) -> None:
        self.layout["header"].update(self.make_header())
        self.layout["summary"].update(self.make_summary())
        self.layout["drones"].update(self.make_drones_table())
        self.layout["map"].update(self.make_map())
        self.layout["events"].update(self.make_event_log())
        self.layout["footer"].update(self.make_footer())
