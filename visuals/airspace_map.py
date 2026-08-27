#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   airspace_map.py                                      :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jay-k <jay-k@student.42.fr>                  +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/25 11:19:02 by jkrishna            #+#    #+#            #
#   Updated: 2026/08/28 00:17:27 by jay-k              ###   ########.fr      #
#                                                                             #
# ########################################################################### #


import random

from rich.text import Text
from typing import Any
from textual.widget import Widget
# from textual.widgets import Static
from textual.color import Color
from textual.events import MouseMove
from core.engine import Engine
from data_models.zone import Zone


class AirspaceMap(Widget):

    """Display the drone airspace map using a Textual widget."""
    DEFAULT_CSS = """
    AirspaceMap {
        width: 100%;
        height: 100%;
        border: round cyan;
        overflow: hidden;
    }
    """

    DRONE_COLORS = [
        "red",
        "blue",
        "green",
        "yellow",
        "#FFA500",
        "magenta",
        "cyan",
        "bright_red",
        "bright_blue",
        "bright_green",
    ]

    def __init__(self, engine: Engine, **kwargs: Any) -> None:
        """Initialize the airspace map.

        Args:
            engine: Simulation engine containing the graph and drones.
            **kwargs: Additional arguments passed to the Textual widget.
        """
        super().__init__(**kwargs)

        self.engine = engine

        # Screen position of zone
        self.zone_positions: dict[tuple[int, int], Zone] = {}

        # Currently hovered zone
        self.hovered_zone: Zone | None = None

        self.mouse_x = 0
        self.mouse_y = 0

        # self.tooltip = HoverTooltip("")
        # self.tooltip.display = False

    # COLOR GUARD #

    def rich_color(self, color: str | None) -> str:
        """Convert a map color to a Textual-compatible color.

        Args:
            color: Color name or hexadecimal color value.

        Returns:
            A valid hexadecimal color string.
        """
        if color == "rainbow":
            color = random.choice([
                "violet", "indigo",
                "blue", "green",
                "yellow", "orange",
                "red"])

        if color is None:
            return "white"

        try:
            return Color.parse(color).hex
        except ValueError:
            return "white"

    #  SCALING  #

    def scale_coordinates(
        self,
        x: float,
        y: float,
        min_x: float,
        max_x: float,
        min_y: float,
        max_y: float,
        width: int,
        height: int,
    ) -> tuple[int, int]:
        """Scale graph coordinates to positions on the terminal canvas.

        Args:
            x: X coordinate of the zone.
            y: Y coordinate of the zone.
            min_x: Minimum X coordinate in the graph.
            max_x: Maximum X coordinate in the graph.
            min_y: Minimum Y coordinate in the graph.
            max_y: Maximum Y coordinate in the graph.
            width: Width of the terminal canvas.
            height: Height of the terminal canvas.

        Returns:
            The scaled screen coordinates as an (x, y) tuple.
        """
        # extra space around the map
        x_range = max_x - min_x
        y_range = max_y - min_y

        padding_x = 4
        padding_y = 2

        usable_width = max(width - (padding_x * 2) - 1, 1)
        usable_height = max(height - (padding_y * 2) - 1, 1)

        if x_range == 0:
            screen_x = width // 2
        else:
            screen_x = padding_x + int(
                ((x - min_x) / x_range)
                * usable_width
            )

        if y_range == 0:
            screen_y = height // 2
        else:
            screen_y = padding_y + int(
                ((y - min_y) / y_range)
                * usable_height
            )

        screen_y = (height - 1 - screen_y)

        return screen_x, screen_y

    # DRAW LINE BETWEEN ZONE #

    def draw_line(
        self,
        canvas: list[list[Text]],
        x1: int,
        y1: int,
        x2: int,
        y2: int,
    ) -> None:
        """Draw a connection between two zones on the canvas.

        Args:
            canvas: Two-dimensional canvas used for rendering.
            x1: X coordinate of the first zone.
            y1: Y coordinate of the first zone.
            x2: X coordinate of the second zone.
            y2: Y coordinate of the second zone.
        """
        width = len(canvas[0])
        height = len(canvas)

        dx = x2 - x1
        dy = y2 - y1

        steps = max(abs(dx), abs(dy))

        if steps == 0:
            return

        for step in range(steps + 1):

            x = round(x1 + (dx * step / steps))
            y = round(y1 + (dy * step / steps))

            if not (0 <= x < width and 0 <= y < height):
                continue

            if abs(dx) > abs(dy):
                character = "─"
            elif abs(dx) < abs(dy):
                character = "|"
            else:
                if (dx * dy) > 0:
                    character = "\\"
                else:
                    character = "/"
            canvas[y][x] = Text(
                character,
                style="dim white",
            )

    #  DRAW ZONE  #

    def draw_zone(
        self,
        canvas: list[list[Text]],
        zone: Zone,
        x: int,
        y: int,
    ) -> None:
        """Draw a zone symbol at its screen position.

        Args:
            canvas: Two-dimensional canvas used for rendering.
            zone: Zone to draw.
            x: X coordinate on the canvas.
            y: Y coordinate on the canvas.
        """
        width = len(canvas[0])
        height = len(canvas)

        if not (0 <= x < width and 0 <= y < height):
            return

        # ZONE SYMBOL

        if zone == self.engine.graph.start_hub:
            symbol = "S"

        elif zone == self.engine.graph.end_hub:
            symbol = "E"

        elif zone.type.lower() == "restricted":
            symbol = "R"

        elif zone.type.lower() == "priority":
            symbol = "P"

        elif zone.type.lower() == "normal":
            symbol = "N"

        elif zone.type.lower() == "blocked":
            symbol = "B"

        else:
            symbol = "U"

        style = self.rich_color(zone.color)

        # ADDING ZONE TO CANVAS
        canvas[y][x] = Text(symbol, style=style)

        # # ADDING ZONE NAME
        # name = str(zone.name)

        # name_x = x + 2

        # for index, chars in enumerate(name):

        #     target_x = name_x + index
        #     if 0 <= target_x < width and 0 <= y < height:

        #         canvas[y][target_x] = Text(
        #             chars,
        #             style="bold white"
        #         )

    #  DRAW DRONES  #

    def draw_drones(
        self,
        canvas: list[list[Text]],
        positions: dict[Zone, tuple[int, int]]
    ) -> None:
        """Draw all drones at their current or interpolated positions.

        Args:
            canvas: Two-dimensional canvas used for rendering.
            positions: Mapping of zones to screen coordinates.
        """
        width = len(canvas[0])
        height = len(canvas)

        for drone in self.engine.drones_stat:

            if (
                drone.current_zone
                == self.engine.graph.end_hub
                # and drone.visual_destination is None
            ):
                if drone.current_zone in positions:
                    position = positions[drone.current_zone]
                else:
                    continue

            else:
                # DETERMINE DRONE POSITION:

                position = None

                # Drone travelling through connection
                if (
                    position is None
                    and drone.current_connection is not None
                    and drone.destination is not None
                ):
                    start = drone.current_zone
                    destination = drone.destination

                    if start in positions and destination in positions:
                        start_x, start_y = positions[start]
                        end_x, end_y = positions[destination]

                        progress = getattr(drone, "visual_progress", 0.0)

                        x = int(start_x + (end_x - start_x) * progress)
                        y = int(start_y + (end_y - start_y) * progress)
                        position = (x, y)

                # Normal visual movement
                if position is None:
                    if (
                        drone.visual_destination is not None
                        and drone.previous_zone is not None
                    ):

                        previous = drone.previous_zone
                        current = drone.visual_destination

                        if (
                            previous in positions
                            and current in positions
                        ):
                            start_x, start_y = positions[previous]
                            end_x, end_y = positions[current]

                            progress = getattr(drone, "visual_progress", 0.0)

                            x = int(start_x + (end_x - start_x) * progress)
                            y = int(start_y + (end_y - start_y) * progress)

                            position = (x, y)

                    # Drone sitting in a zone
                    if position is None:

                        if drone.current_zone not in positions:
                            continue

                        position = positions[drone.current_zone]
                x, y = position

                if not (0 <= x < width and 0 <= y < height):
                    continue

                color = self.DRONE_COLORS[
                    (drone.id - 1) % len(self.DRONE_COLORS)]
                label = f"D{drone.id}"

                # DRAW DRONE ID
                for index, chars in enumerate(label):

                    target_x = x + index
                    if 0 <= target_x < width and 0 <= y < height:
                        canvas[y][target_x] = Text(
                            chars,
                            style=f"bold {color}"
                        )

    #    RENDER    #

    def render(self) -> Text:
        """Render the complete airspace map.

        Returns:
            A Textual Text object containing the rendered map.
        """

        width = self.size.width
        height = self.size.height

        # Textual may call render before the widget has recieved
        # a useful size.

        if width < 10 or height < 5:
            return Text("Loading airspace map...")

        zones = self.engine.graph.zones

        if not zones:
            return Text("No zones available.")

        # Graph coordinate bounds

        coordinates = [zone.coordinates for zone in zones]

        min_x = min(coord[0] for coord in coordinates)
        max_x = max(coord[0] for coord in coordinates)
        min_y = min(coord[1] for coord in coordinates)
        max_y = max(coord[1] for coord in coordinates)

        # Create canvas

        canvas = [
            [Text(" ") for _ in range(width)]
            for _ in range(height)
        ]

        # Calculate every zone's screen position
        positions = {}

        for zone in zones:
            x, y = zone.coordinates

            screen_positions = self.scale_coordinates(
                x,
                y,
                min_x,
                max_x,
                min_y,
                max_y,
                width,
                height,
            )

            positions[zone] = screen_positions

        # Zone position for mouse interaction
        self.zone_positions = {
            position: zone
            for zone, position in positions.items()
        }
        # FIRST Draw connections

        for connection in self.engine.graph.connections:
            zone_a = connection.zone_a
            zone_b = connection.zone_b

            if zone_a not in positions:
                continue

            if zone_b not in positions:
                continue

            x1, y1 = positions[zone_a]
            x2, y2 = positions[zone_b]

            self.draw_line(
                canvas,
                x1,
                y1,
                x2,
                y2,
            )

        # SECOND Draw zones

        for zone in zones:
            x, y = positions[zone]

            self.draw_zone(
                canvas,
                zone,
                x,
                y,
            )

        # Last Draw drones

        self.draw_drones(canvas, positions)

        # DRAW HOVER POPUP

        if self.hovered_zone is not None:
            zone = self.hovered_zone

            popup_lines = [
                f"{zone.name}",
                f"Cost: {zone.cost}",
                (
                    f"Capacity: {self.engine.zone_occupancy[zone]}"
                    f"/{zone.max_drones}"
                ),
                f"Coordinates: {zone.coordinates}",
            ]

            popup_width = max(len(line) for line in popup_lines) + 2
            popup_height = len(popup_lines) + 2

            # keep popup within the map
            popup_x = self.mouse_x + 2
            popup_y = self.mouse_y + 1

            if popup_x + popup_width >= width:
                popup_x = max(0, self.mouse_x - popup_width - 1)

            if popup_y + popup_height >= height:
                popup_y = max(0, self.mouse_y - popup_height - 1)

            # Top border
            if 0 <= popup_y < height:
                for px in range(popup_width):
                    if 0 <= popup_x + px < width:
                        canvas[popup_y][popup_x + px] = Text("─")

            # Content
            for row_index, line in enumerate(popup_lines, start=1):
                py = popup_y + row_index

                if not (0 <= py < height):
                    continue

                for px in range(popup_width):
                    target_x = popup_x + px

                    if not (0 <= target_x < width):
                        continue
                    if px == 0 or px == popup_width - 1:
                        canvas[py][target_x] = Text("|")
                    else:
                        char_index = px - 1

                        if char_index < len(line):
                            canvas[py][target_x] = Text(
                                line[char_index],
                                style="bold white",
                            )
                        else:
                            canvas[py][target_x] = Text(" ")
            # Bottom border
            bottom_y = popup_y + popup_height - 1

            if 0 <= bottom_y < height:
                for px in range(popup_width):
                    if 0 <= popup_x + px < width:
                        canvas[bottom_y][popup_x + px] = Text("─")

        result = Text()

        for row in canvas:
            for cell in row:
                result.append(cell)
            result.append("\n")

        return result

    # Mouse Event #

    def on_mouse_move(self, event: MouseMove) -> None:
        """Update the hovered zone when the mouse moves.

        Args:
            event: Textual mouse-movement event containing the cursor position.
        """
        self.mouse_x = event.offset.x
        self.mouse_y = event.offset.y

        hover_radius = 2
        nearest_zone: Zone | None = None
        nearest_distance = float("inf")

        for (zone_x, zone_y), zone in self.zone_positions.items():
            dx = self.mouse_x - zone_x
            dy = self.mouse_y - zone_y

            dist = (dx)**2 + (dy)**2

            if dist <= hover_radius**2:
                if dist < nearest_distance:
                    nearest_distance = dist
                    nearest_zone = zone

        self.hovered_zone = nearest_zone

        self.refresh()

    # Refresh #

    def refresh_map(self) -> None:
        """Refresh the map after the simulation state changes."""
        self.refresh()
