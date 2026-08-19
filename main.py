# #!/usr/bin/env python3


# import sys
# import traceback

# from parser.map_parser import Parser
# from core.engine import Engine
# from visuals.visual_generator import Dashboard


# def main() -> None:
#     if len(sys.argv) != 2:
#         print("Usage is: python3 main.py <path/to/map.txt>")
#         sys.exit(1)

#     parsed = Parser(sys.argv[1])
#     graph_object = parsed.parser()

#     machine = Engine(graph_object)

#     dashboard = Dashboard(machine)
#     dashboard.run()


# if __name__ == "__main__":
#     try:
#         main()
#     except Exception:
#         traceback.print_exc()
#         sys.exit(1)
