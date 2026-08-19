# #!/usr/bin/env python3

# from textual.app import App, ComposeResult
# from textual.containers import Container, Horizontal
# from textual.widgets import DataTable, Footer, Header, Static

# from core.engine import Engine
# from visuals.airspace_map import AirspaceMap


# # --------------------------------------------------------------------------#
# # Event Log
# # --------------------------------------------------------------------------#

# class EventLog(Static):
#     """Display the simulation event log."""

#     DEFAULT_CSS = """
#     EventLog {
#         width: 100%;
#         height: 100%;
#         padding: 1;
#         overflow-y: auto;
#     }
#     """

#     def __init__(
#         self,
#         engine: Engine,
#         **kwargs,
#     ) -> None:
#         super().__init__(**kwargs)

#         self.engine = engine

#     def update_log(self) -> None:
#         """Update the displayed events."""

#         events = self.engine.event_log[-10:]

#         if not events:
#             self.update("No events yet.")
#             return

#         self.update(
#             "\n".join(
#                 str(event)
#                 for event in events
#             )
#         )


# # ------------------------------------------------------------------------- #
# # Summary
# # ------------------------------------------------------------------------- #

# class Summary(Static):
#     """Display simulation statistics."""

#     DEFAULT_CSS = """
#     Summary {
#         width: 100%;
#         height: 100%;
#         padding: 1;
#         overflow: hidden;
#     }
#     """

#     def __init__(
#         self,
#         engine: Engine,
#         **kwargs,
#     ) -> None:
#         super().__init__(**kwargs)

#         self.engine = engine

#     def update_summary(self) -> None:
#         """Update simulation statistics."""

#         total_drones = (
#             self.engine.graph.total_drones
#         )

#         drones_in_connections = sum(
#             len(drones)
#             for drones in self.engine.connection_stat.values()
#         )

#         drones_in_transit = 0

#         for zone in self.engine.zone_stat:

#             if zone not in (
#                 self.engine.graph.start_hub,
#                 self.engine.graph.end_hub,
#             ):
#                 drones_in_transit += len(
#                     self.engine.zone_stat[zone]
#                 )

#         completed_drones = (
#             self.engine.zone_occupancy.get(
#                 self.engine.graph.end_hub,
#                 0,
#             )
#         )

#         self.update(
#             f"Total Drones\n"
#             f"  {total_drones}\n\n"
#             f"Drones In Connections\n"
#             f"  {drones_in_connections}\n\n"
#             f"Drones In Transit\n"
#             f"  {drones_in_transit}\n\n"
#             f"Completed Drones\n"
#             f"  {completed_drones}\n\n"
#             f"Total Turns\n"
#             f"  {self.engine.ticks}\n\n"
#             f"Total path_cost\n"
#             f"  {self.engine.total_path_cost}"
#         )


# # ------------------------------------------------------------------------- #
# # Drone Table
# # ------------------------------------------------------------------------- #

# class DroneTable(DataTable):
#     """Display the current state of all drones."""

#     DEFAULT_CSS = """
#     DroneTable {
#         width: 100%;
#         height: 100%;
#     }
#     """

#     def __init__(
#         self,
#         engine: Engine,
#         **kwargs,
#     ) -> None:
#         super().__init__(**kwargs)

#         self.engine = engine

#     def on_mount(self) -> None:
#         """Create table columns."""

#         self.add_columns(
#             "DRONE ID",
#             "CURRENT ZONE",
#             "PATH (NEXT -> ...)",
#             "STATUS",
#             "WAITING",
#         )

#     def update_table(self) -> None:
#         """Refresh the drone table."""

#         self.clear()

#         for drone in self.engine.drones_stat:

#             path = self.engine.drones_stat[drone]

#             # drones_stat stores the path as a deque.
#             # Convert to a list before slicing.
#             path_list = list(path)

#             if len(path_list) > 1:

#                 drone_path = " -> ".join(
#                     zone.name
#                     for zone in path_list[1:]
#                 )

#             else:
#                 drone_path = ""

#             # ------------------------------------------------------------- #
#             # Status
#             # ------------------------------------------------------------- #

#             if (
#                 drone.current_zone
#                 == self.engine.graph.end_hub
#             ):
#                 status = "IN_END_ZONE"
#             else:
#                 status = "IN_TRANSIT"

#             # ------------------------------------------------------------- #
#             # Waiting
#             # --------------------------------------------------------------#

#             if drone in self.engine.waiting:
#                 waiting = "YES"
#             else:
#                 waiting = "NO"

#             self.add_row(
#                 str(drone.id),
#                 str(drone.current_zone.name),
#                 drone_path,
#                 status,
#                 waiting,
#             )


# # ------------------------------------------------------------------------- #
# # Dashboard
# # ------------------------------------------------------------------------- #

# class Dashboard(App):
#     """Main Textual application."""

#     TITLE = "FlyIn - Drone Traffic Simulation"

#     CSS = """
#     /* ------------------------------------------------------------------ */
#     /* Whole application                                                  */
#     /* ------------------------------------------------------------------ */

#     Screen {
#         layout: vertical;
#     }

#     /* ------------------------------------------------------------------ */
#     /* Main dashboard                                                     */
#     /* ------------------------------------------------------------------ */

#     #main {
#         width: 100%;
#         height: 1fr;
#         layout: vertical;
#     }

#     /* ------------------------------------------------------------------ */
#     /* Top section                                                        */
#     /* ------------------------------------------------------------------ */

#     #top {
#         width: 100%;
#         height: 2fr;
#         layout: horizontal;
#     }

#     /* ------------------------------------------------------------------ */
#     /* Airspace map                                                       */
#     /* ------------------------------------------------------------------ */

#     #map {
#         width: 3fr;
#         height: 100%;
#     }

#     /* ------------------------------------------------------------------ */
#     /* Event log                                                          */
#     /* ------------------------------------------------------------------ */

#     #events {
#         width: 1fr;
#         height: 100%;
#         border: round yellow;
#         padding: 1;
#         overflow-y: auto;
#     }

#     /* ------------------------------------------------------------------ */
#     /* Bottom section                                                     */
#     /* ------------------------------------------------------------------ */

#     #bottom {
#         width: 100%;
#         height: 1fr;
#         layout: horizontal;
#     }

#     /* ------------------------------------------------------------------ */
#     /* Drone table                                                        */
#     /* ------------------------------------------------------------------ */

#     #drones {
#         width: 6fr;
#         height: 100%;
#         border: round green;
#     }

#     /* ------------------------------------------------------------------ */
#     /* Summary                                                            */
#     /* ------------------------------------------------------------------ */

#     #summary {
#         width: 1fr;
#         height: 100%;
#         border: round magenta;
#         padding: 1;
#         overflow: hidden;
#     }
#     """

#     def __init__(
#         self,
#         engine: Engine,
#     ) -> None:
#         super().__init__()

#         self.engine = engine

#     # --------------------------------------------------------------------- #
#     # Layout
#     # --------------------------------------------------------------------- #

#     def compose(self) -> ComposeResult:
#         """Build the dashboard layout."""

#         yield Header()

#         with Container(id="main"):

#             # ------------------------------------------------------------- #
#             # Top
#             # ------------------------------------------------------------- #

#             with Horizontal(id="top"):

#                 yield AirspaceMap(
#                     self.engine,
#                     id="map",
#                 )

#                 yield EventLog(
#                     self.engine,
#                     id="events",
#                 )

#             # ------------------------------------------------------------- #
#             # Bottom
#             # ------------------------------------------------------------- #

#             with Horizontal(id="bottom"):

#                 yield DroneTable(
#                     self.engine,
#                     id="drones",
#                 )

#                 yield Summary(
#                     self.engine,
#                     id="summary",
#                 )

#         yield Footer()

#     # --------------------------------------------------------------------- #
#     # Mount
#     # --------------------------------------------------------------------- #

#     def on_mount(self) -> None:
#         """Initialize the dashboard."""

#         # Update once immediately so the user doesn't
#         # have to wait for the first simulation tick.
#         self.update_dashboard()

#         # Run one simulation step every second.
#         self.set_interval(
#             1.0,
#             self.run_simulation,
#         )

#     # --------------------------------------------------------------------- #
#     # Simulation
#     # --------------------------------------------------------------------- #

#     def run_simulation(self) -> None:
#         """Run one simulation tick."""

#         if self.engine.is_finished():
#             self.exit()
#             return

#         self.engine.simulation()

#         self.update_dashboard()

#     # --------------------------------------------------------------------- #
#     # Update dashboard
#     # --------------------------------------------------------------------- #

#     def update_dashboard(self) -> None:
#         """Refresh every dashboard component."""

#         # --------------------------------------------------------------- #
#         # Event log
#         # --------------------------------------------------------------- #

#         event_log = self.query_one(
#             "#events",
#             EventLog,
#         )

#         event_log.update_log()

#         # --------------------------------------------------------------- #
#         # Drone table
#         # --------------------------------------------------------------- #

#         drone_table = self.query_one(
#             "#drones",
#             DroneTable,
#         )

#         drone_table.update_table()

#         # --------------------------------------------------------------- #
#         # Summary
#         # --------------------------------------------------------------- #

#         summary = self.query_one(
#             "#summary",
#             Summary,
#         )

#         summary.update_summary()

#         # --------------------------------------------------------------- #
#         # Airspace map
#         # --------------------------------------------------------------- #

#         airspace_map = self.query_one(
#             "#map",
#             AirspaceMap,
#         )

#         airspace_map.refresh_map()
