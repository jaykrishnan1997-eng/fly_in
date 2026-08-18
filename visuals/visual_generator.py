#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   visual_generator.py                                  :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jay-k <jay-k@student.42.fr>                  +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/15 13:00:33 by jkrishna            #+#    #+#            #
#   Updated: 2026/08/18 21:51:32 by jay-k              ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import sys
import time
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from core.engine import Engine

# ┌──────────────────────────────────────────────────────────────┐
# │ HEADER                                                       │
# ├──────────────────────────────────┬───────────────────────────┤
# │                                  │ EVENT LOGS                │
# │                                  |                           |
# │           AIRSPACE MAP           |                           │
# │                                  │                           │
# │                                  │                           │
# ├──────────────────────────────────┴───────────────────────────┤
# │ DRONES                           │ SUMMARY                   │
# ├──────────────────────────────────┴───────────────────────────┤
# │ FOOTER / CONTROLS                                            │
# └──────────────────────────────────────────────────────────────┘


class Dashboard:
    def __init__(self, engine: Engine) -> None:

        self.engine = engine
        self.layout = self.make_layout()
        self.completed_drones: set[int] = set()

        self.drone_colors = [
            "red",
            "blue",
            "green",
            "yellow",
            "magenta",
            "cyan",
            "bright_red",
            "bright_blue",
            "bright_green",
        ]

    def make_layout(self) -> Layout:
        """Define the layout."""
        layout = Layout(name="root")

        # Vertical: header, main, footer
        layout.split(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3),
        )
        # main: top, bottom
        layout["main"].split_column(
            Layout(name="top", ratio=2),
            Layout(name="bottom", ratio=1),
        )
        # top: map, event log
        layout["top"].split_row(
            Layout(name="map", ratio=3),
            Layout(name="events", ratio=1),
        )
        # Bottom: drones, summary
        layout["bottom"].split_row(
            Layout(name="drones", ratio=6),
            Layout(name="summary", ratio=1),
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
            "Total Turns",
            str(self.engine.ticks),
        )
        table.add_row(
            "Total path_cost",
            str(self.engine.total_path_cost),
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
                        drone_path += (
                            f"{self.engine.drones_stat[drone][i].name} -> "
                        )
                    else:
                        drone_path += str(
                            self.engine.drones_stat[drone][i].name)

            if drone.current_zone == self.engine.graph.end_hub:
                if drone.id in self.completed_drones:
                    continue
                self.completed_drones.add(drone.id)
                status = "IN_END_ZONE"
            else:
                status = "IN_TRANSIT"

            if drone in self.engine.waiting:
                waiting_status = "YES"
            else:
                waiting_status = "NO"
            table.add_row(
                str(drone.id),
                str(drone.current_zone.name),
                drone_path,
                status,
                str(waiting_status),
            )
        return Panel(table, title="Drones")

    def make_event_log(self) -> Panel:
        table = Table.grid(expand=True)

        visible_events = self.engine.event_log[-10:]

        for event in visible_events:
            table.add_row(event)

        return Panel(table, title="Event Log")

    def make_footer(self) -> Panel:
        return Panel("Controls")

    # The core visual(the drones transit itself)
    def make_map(self, progress: float = 1.0) -> Panel:
        width = 70
        height = 20

        padding = 2

        zones = self.engine.graph.zones

        if not zones:
            return Panel("", title="Airspace Map")

        min_x = min(zone.coordinates[0] for zone in zones)
        max_x = max(zone.coordinates[0] for zone in zones)

        min_y = min(zone.coordinates[1] for zone in zones)
        max_y = max(zone.coordinates[1] for zone in zones)

        # to prevent division by zero
        x_range = max_x - min_x or 1
        y_range = max_y - min_y or 1

        # graph coordinates to screen coordinates
        def scale_x(x: float) -> int:
            return int(
                (x - min_x) * ((width - 1) - (2 * padding))
                / x_range
            ) + padding

        def scale_y(y: int) -> int:
            return int(
                (y - min_y) * ((height - 1) - (2 * padding))
                / y_range
            ) + padding

        # empty canvas
        canvas = [
            [Text(" ") for _ in range(width)]
            for _ in range(height)
        ]

        # CONNECTION

        for connection in self.engine.graph.connections:
            x1 = scale_x(connection.zone_a.coordinates[0])
            y1 = scale_y(connection.zone_a.coordinates[1])
            x2 = scale_x(connection.zone_b.coordinates[0])
            y2 = scale_y(connection.zone_b.coordinates[1])

            if y1 == y2:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    canvas[y1][x] = Text("─", style="dim")

            elif x1 == x2:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    canvas[y][x1] = Text("|", style="dim")

        # ZONES

        for zone in zones:
            x = scale_x(zone.coordinates[0])
            y = scale_y(zone.coordinates[1])

            if not (0 <= x < width and 0 <= y < height):
                continue

            if zone == self.engine.graph.start_hub:
                symbol = "S"
                style = zone.color or "white"
            elif zone == self.engine.graph.end_hub:
                symbol = "E"
                style = zone.color or "white"
            elif zone.cost == 2:
                symbol = "R"
                style = zone.color or "white"
            elif zone.cost == 1:
                symbol = "P"
                style = zone.color or "white"
            elif zone.cost == sys.maxsize:
                symbol = "B"
                style = zone.color or "white"
            else:
                symbol = "U"
                style = zone.color or "white"

            canvas[y][x] = Text(symbol, style=style)

            # Zone name next to zone
            name = zone.name[:10]

            name_x = x + 2

            if name_x + len(name) < width:
                for i, char in enumerate(name):
                    canvas[y][name_x + i] = Text(
                        char,
                        style="bold white"
                    )
        # DRONES

        for drone in self.engine.drones_stat:

            if (
                drone.current_zone == self.engine.graph.end_hub
                and drone.visual_destination is None
            ):
                continue

            # Drone in connection for restricted zone

            if (
                drone.current_connection is not None
                and drone.destination is not None
            ):
                start = drone.current_zone
                destination = drone.destination

                start_x = scale_x(start.coordinates[0])
                start_y = scale_y(start.coordinates[1])

                end_x = scale_x(destination.coordinates[0])
                end_y = scale_y(destination.coordinates[1])

                x = int(
                    start_x + (end_x - start_x) * progress
                )

                y = int(
                    start_y + (end_y - start_y) * progress
                )

            # Normal movement
            elif (
                drone.previous_zone is not None
                and drone.visual_destination is not None
            ):

                previous = drone.previous_zone
                current = drone.visual_destination

                start_x = scale_x(previous.coordinates[0])
                start_y = scale_y(previous.coordinates[1])

                end_x = scale_x(current.coordinates[0])
                end_y = scale_y(current.coordinates[1])

                x = int(
                    start_x + (end_x - start_x) * progress
                )

                y = int(
                    start_y + (end_y - start_y) * progress
                )

            else:
                x = scale_x(drone.current_zone.coordinates[0])
                y = scale_y(drone.current_zone.coordinates[1])

            if 0 <= x < width and 0 <= y < height:

                color = self.drone_colors[
                    (drone.id - 1) % len(self.drone_colors)
                ]

                canvas[y][x] = Text(
                    f"D{drone.id}",
                    style=f"bold {color}"
                )

        # Convert canvas to rich text

        lines = []

        for row in canvas:
            line = Text()

            for cell in row:
                line.append(cell)

            lines.append(line)

        return Panel(
            Text("\n").join(lines),
            title="Airspace Map",
        )

    def animate_map(self) -> None:
        frames = 6

        for frame in range(1, frames + 1):
            progress = frame / frames

            self.layout["map"].update(
                self.make_map(progress)
            )

            time.sleep(0.08)

        for drone in self.engine.drones_stat:
            drone.previous_zone = None
            drone.visual_destination = None

    def update(self) -> None:
        self.layout["header"].update(self.make_header())
        self.layout["summary"].update(self.make_summary())
        self.layout["drones"].update(self.make_drones_table())
        self.layout["map"].update(self.make_map(0.0))
        self.layout["events"].update(self.make_event_log())
        self.layout["footer"].update(self.make_footer())

        self.animate_map()
