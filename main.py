#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   main.py                                              :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/03 14:17:07 by jkrishna            #+#    #+#            #
#   Updated: 2026/08/18 12:58:31 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import sys
import time
import traceback

from rich.live import Live
from parser.map_parser import Parser
from core.engine import Engine
from visuals.visual_generator import Dashboard


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage is: python3 main.py <path/to/map.txt>")
        sys.exit(1)

    parsed = Parser(sys.argv[1])
    graph_object = parsed.parser()

    machine = Engine(graph_object)
    dashboard = Dashboard(machine)

    with Live(
        dashboard.layout,
        refresh_per_second=10,
        screen=True,
    ) as live:
        while not machine.is_finished():
            machine.simulation()

            dashboard.update()
            live.update(dashboard.layout)

            time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
