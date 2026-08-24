#!/usr/bin/env python3


import sys
import traceback

from parser.map_parser import Parser
from core.engine import Engine
from visuals.visual_generator import Dashboard


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage is: python3 main.py <path/to/map.txt>")
        sys.exit(1)

    map_path = sys.argv[1]
    if ".txt" not in map_path and "maps/" not in map_path:
        raise ValueError("Usage is: python3 main.py <path/to/map.txt>")

    parsed = Parser(map_path)
    graph_object = parsed.parser()

    machine = Engine(graph_object)

    dashboard = Dashboard(machine, map_path)
    dashboard.run()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
