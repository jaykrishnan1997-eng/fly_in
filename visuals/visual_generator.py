#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   visual_generator.py                                  :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/15 13:00:33 by jkrishna            #+#    #+#            #
#   Updated: 2026/08/15 14:44:13 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

# This is a from a tutorial on rich i am recreating
# it ,learn how it works and change it into a formalt i want

# from datetime import datetime

# from rich import box
# from rich.align import Align
# from rich.console import Console, RenderGroup
# from rich.layout import Layout
# from rich.panel import Panel
# from rich.table import Table
# from rich.text import text

# console = Console()


# def make_layout() -> Layout:
#     """Define the layout."""
#     layout = Layout(name="root")

#     layout.split(
#         Layout(name="header", size=3),
#         Layout(name="main", size=1),
#         Layout(name="footer", size=7),
#     )
#     layout["main"].split(
#         Layout(name="side"),
#         Layout(name="body", ratio=2, minimum_size=60),
#         direction="horizontal",
#     )
#     layout["side"].split(Layout(name="box1"), Layout(name="box2"))
#     return layout


# def make_sponsor_message() -> Panel:
#     """Some example content."""
#     sponsor_message = Table.grid(padding=1)
#     sponsor_message.add_column(style="green", justify="right")
#     sponsor_message.add_column(no_wrap=True)
#     sponsor_message.add_row(
#         "Sponsor me",
#         "[u blue link=https://google.com]"
#     )
#     sponsor_message.add_row(
#         "Buy me a coffee:",
#         "[u blue link=https://google.com]"
#     )
#     sponsor_message.add_row(
#         "Twitter:",
#         "[u blue link=https://google.com]"
#     )
#     intro_message = Text.from_makeup(
#         """Support my work"""
#     )


#     message = Table.grid(padding=1)
#     message.add_column()
#     message.add_column(no_wrap=True)
#     message.add_row(intro_message, sponsor_message)

#     message_panel = Panel(
#         Align.center(
#             RenderGroup(intro_message, "\n", Align.center(sponsor_message)),
#             vertical="middle",
#         ),
#         box=box.ROUNDED,
#         padding=(1, 2),
#         title="[b red]Thanks for trying out Rich!",
#         border_style="bright_blue",
#     )
#     return message_panel


# Class Header:
#     """Display header with clock."""
#
#      def __rich__(self) -> Panel:
#         grid = Table.grid(expand=True)
#         grid.add_column(justify="center", ratio=1)
#         grid.add_column(justify="right")
#         grid.add_row(
#             "[b]Rich[\b] Layout application",
#             datetime.now().ctime().replace(":", "[blink]:[/]"),
#         )
#         return Panel(grid, style="white on blue")
#
#
#     def make_syntax() -> Syntax:
#         ccode = """\
#     def
#         """
