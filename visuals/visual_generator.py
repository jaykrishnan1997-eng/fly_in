#!/usr/bin/env python3

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import DataTable, Footer, Header, Static

from core.engine import Engine
from visuals.airspace_map import AirspaceMap


# ########### #
#  EVENT LOG  #
# ########### #

class EventLog(Static):
    # Display the simulation event log
    TITLE = "EVENT LOG"

    DEFAULT_CSS = """
    EvantLog {
        width: 100;
        height: 100;
        padding: 1;
        overflow-y: auto;
    }
    """

    def __init__(
        self,
        engine: Engine,
        **kwargs: object,
    ) -> None:
        super().__init__(**kwargs)

        self.engine = engine

    def update_log(self) -> None:
        # update the displayed events.

        events = self.engine.event_log[-10:]

        if not events:
            self.update("No events yet.")
            return

        self.update(
            "\n".join(
                str(event)
                for event in events
            )
        )


# ########### #
#   SUMMARY   #
# ########### #

class Summary(Static):
    # Display simulattion statistics.
    TITLE = "SUMMARY"

    DEFAULT_CSS = """
    Summary {
        width: 100%;
        height: 100%;
        padding: 1;
        overflow: hidden;
    }
    """

    def __init__(
        self,
        engine: Engine,
        **kwargs: object,
    ) -> None:
        super().__init__(**kwargs)

        self.engine = engine

    def update_summary(self) -> None:
        # update simulation staticstics.abs
        total_drones = self.engine.graph.total_drones

        drones_in_connections = sum(
            len(drones)
            for drones in self.engine.connection_stat.values()
        )

        drones_in_transit = 0

        for zone in self.engine.zone_stat:
            if zone not in (
                self.engine.graph.start_hub,
                self.engine.graph.end_hub,
            ):
                drones_in_transit += len(
                    self.engine.zone_stat[zone]
                )

        completed_drones = (
            self.engine.zone_occupancy.get(self.engine.graph.end_hub, 0)
        )

        self.update(
            f"Total Drones: {total_drones}\n"
            f"Drones in Connection: {drones_in_connections}\n"
            f"Drones in Transit: {drones_in_transit}\n"
            f"Completed Drones: {completed_drones}\n"
            f"Total path cost: {self.engine.total_path_cost}\n"
            f"Total turns: {self.engine.ticks}\n"
        )


# ############# #
#  DRONE TABLE  #
# ############# #

class DroneTable(DataTable):
    # Display the current state of all drones.

    TITLE = "DRONE TABLE"

    DEFAULT_CSS = """
    Dronetbale {
        width: 100%;
        height: 100%;
    }
    """

    def __init__(
        self,
        engine: Engine,
        **kwargs: object,
    ) -> None:
        super().__init__(**kwargs)

        self.engine = engine

    def on_mount(self) -> None:
        # Create table columns.abs

        self.add_columns(
            "DRONE_ID",
            "CURRENT ZONE",
            "PATH (NEXT -> ...)",
            "STATUS",
            "WAITING",
        )

    def update_table(self) -> None:
        # Refresh the drone table.abs

        self.clear()

        for drone in self.engine.drones_stat:
            path = self.engine.drones_stat[drone]

            # Convert the list before slicing since
            # drones_stat stores path as deque
            path_list = list(path)

            if len(path_list) > 1:

                drone_path = " -> ".join(
                    zone.name
                    for zone in path_list[1:]
                )
            else:
                drone_path = ""

            # STATUS
            if drone.current_zone == self.engine.graph.end_hub:
                status = "IN_END_ZONE"
            else:
                status = "IN_TRANSIT"

            # WAITING
            if drone in self.engine.waiting:
                waiting = "YES"
            else:
                waiting = "NO"

            self.add_row(
                str(drone.id),
                str(drone.current_zone.name),
                drone_path,
                status,
                waiting,
            )


# ############# #
#   DASHBOARD   #
# ############# #

class Dashboard(App):

    # Main Textual application.
    TITLE = "FlyIn - Drone Traffic Simulation"

    CSS = """
    Screen {
        layout: vertical
    }

    #main {
        width: 100%;
        height: 1fr;
        layout: vertical;
    }

    #top {
        width: 100%;
        height: 2fr;
        layout: horizontal;
    }

    /* AIRSPACE MAP */
    #map {
        width: 3fr;
        height: 100%;
    }

    /* EVENT LOG */
    #events {
        width: 1fr;
        height: 100%;
        border: round yellow;
        padding: 1;
        overflow-y: auto;
    }

    /* BOTTOM SECTION */
    #bottom {
        width: 100%;
        height: 1fr;
        layout: horizontal;
    }

    /* DRONE TABLE */
    #drones {
        width: 6fr;
        height: 100%;
        border: round green;
    }

    /* SUMMARY */
    #summary {
        width: 1fr;
        height: 100%;
        border: round magenta;
        padding: 1;
        overflow: hidden;
    }
    """

    def __init__(
        self,
        engine: Engine,
    ) -> None:
        super().__init__()

        self.engine = engine

    # LAYOUT
    def compose(self) -> ComposeResult:
        # Build the dashboard layout.

        yield Header()

        with Container(id="main"):

            # TOP
            with Horizontal(id="top"):

                yield AirspaceMap(
                    self.engine,
                    id="map",
                )

                yield EventLog(
                    self.engine,
                    id="events",
                )

            # BOTTOM
            with Horizontal(id="bottom"):

                yield DroneTable(
                    self.engine,
                    id="drones",
                )

                yield Summary(
                    self.engine,
                    id="summary",
                )
        yield Footer()

    # MOUNT
    def on_mount(self) -> None:
        # Initialize the dashboard. Update once immediately so the user
        # doesnt have to wait for the first simulation tick.
        self.update_dashboard()

        # Run one simulation step every second.
        self.set_interval(
            1.0,
            self.run_simulation,
        )

    # SIMULATION
    def run_simulation(self) -> None:
        # Run one simulation tick.
        if self.engine.is_finished():
            self.exit()
            return
        self.engine.simulation()
        self.update_dashboard()

    # UPDATE DASHBOARD
    def update_dashboard(self) -> None:
        # Refresh every dashboard component.

        # EVENT LOG
        event_log = self.query_one(
            "#events",
            EventLog,
        )
        event_log.update_log()

        # DRONE TABLE
        drone_table = self.query_one(
            "#drones",
            DroneTable,
        )
        drone_table.update_table()

        # SUMMARY
        summary = self.query_one(
            "#summary",
            Summary,
        )
        summary.update_summary()

        # AIRSPACE MAP
        airspace_map = self.query_one(
            "#map",
            AirspaceMap,
        )
        airspace_map.refresh_map()
