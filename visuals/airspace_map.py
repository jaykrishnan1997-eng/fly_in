#!/usr/bin/env python3

import sys
from rich.text import Text
from textual.widget import Widget
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


class AirspaceMap(Widget):

    # ######################################## #
    # TEXTUAL WIDGET TO COMPILE THE ENTIRE MAP #
    # ######################################## #
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

    def __init__(
        self,
        engine: Engine,
        **kwargs: object,
    ) -> None:
        super().__init__(**kwargs)

        self.engine = engine

    # ########### #
    # COLOR GUARD #
    # ########### #

    def rich_color(self, color: str | None) -> str:
        # Convert map color orange to format that Textual accept
        if color == "orange":
            return "#FFA500"
        return color or "while"

    # ######### #
    #  SCALING  #
    # ######### #

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

        # extra space around the map
        x_range = max_x - min_x
        y_range = max_y - min_y

        padding_x = 4
        padding_y = 2

        usable_width = max(
            width - (padding_x * 2) - 1,
            1,
        )

        usable_height = max(
            height - (padding_y * 2) - 1,
            1,
        )

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

        screen_y = (
            height
            - 1
            - screen_y
        )

        return screen_x, screen_y

    # ###################### #
    # DRAW LINE BETWEEN ZONE #
    # ###################### #

    def draw_line(
        self,
        canvas: list[list[Text]],
        x1: int,
        y1: int,
        x2: int,
        y2: int,
    ) -> None:

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
    # ########### #
    #  DRAW ZONE  #
    # ########### #

    def draw_zone(
        self,
        canvas: list[list[Text]],
        zone,
        x: int,
        y: int,
    ) -> None:

        width = len(canvas[0])
        height = len(canvas)

        if not (0 <= x < width and 0 <= y < height):
            return

        # ZONE SYMBOL

        if zone == self.engine.graph.start_hub:
            symbol = "S"
            style = self.rich_color(zone.color)

        elif zone == self.engine.graph.end_hub:
            symbol = "E"
            style = self.rich_color(zone.color)

        elif zone.cost == 2:
            symbol = "R"
            style = self.rich_color(zone.color)

        elif zone.cost == 1:
            symbol = "P"
            style = self.rich_color(zone.color)

        elif zone.cost == sys.maxsize:
            symbol = "B"
            style = self.rich_color(zone.color)

        else:
            symbol = "U"
            style = self.rich_color(zone.color)

        # ADDING ZONE TO CANVAS
        canvas[y][x] = Text(
            symbol,
            style=style,
        )

        # ADDING ZONE NAME
        name = str(zone.name)

        name_x = x + 2

        for index, chars in enumerate(name):

            target_x = name_x + index
            if 0 <= target_x < width and 0 <= y < height:

                canvas[y][target_x] = Text(
                    chars,
                    style="bold white"
                )
    # ############# #
    #  DRAW DRONES  #
    # ############# #

    def draw_drones(
        self,
        canvas: list[list[Text]],
        positions: dict
    ) -> None:

        width = len(canvas[0])
        height = len(canvas)

        for drone in self.engine.drones_stat:

            # COMPLETED DRONES DISAPPEAR FROM THE MAP
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

                        progress = getattr(
                            drone,
                            "visual_progress",
                            0.0,
                        )

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

                            progress = getattr(
                                drone,
                                "visual_progress",
                                0.0,
                            )

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
                    (drone.id - 1) % len(self.DRONE_COLORS)
                ]
                label = f"D{drone.id}"

                # DRAW DRONE ID
                for index, chars in enumerate(label):

                    target_x = x + index
                    if 0 <= target_x < width and 0 <= y < height:

                        canvas[y][target_x] = Text(
                            chars,
                            style=f"bold {color}"
                        )

    # ############ #
    #    RENDER    #
    # ############ #
    def render(self) -> Text:
        # Render the complete airspace map

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

        coordinates = [
            zone.coordinates
            for zone in zones
        ]

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
            positions[zone] = self.scale_coordinates(
                x,
                y,
                min_x,
                max_x,
                min_y,
                max_y,
                width,
                height,
            )

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

        self.draw_drones(
            canvas,
            positions,
        )

        # Convert canvas to rich text

        result = Text()

        for row in canvas:
            for cell in row:
                result.append(cell)
            result.append("\n")
        return result

    # ####### #
    # Refresh #
    # ####### #

    def refresh_map(self) -> None:
        # refresh map after a simulation update
        self.refresh()
