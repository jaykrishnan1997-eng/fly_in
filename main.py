#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   main.py                                              :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/03 14:17:07 by jkrishna            #+#    #+#            #
#   Updated: 2026/08/05 15:34:15 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import sys
from parser.map_parser import Parser
import traceback


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage is: python3 main.py <path/to/map.txt>")
        sys.exit(1)

    parsed = Parser(sys.argv[1])
    graph_object = parsed.parser()
    print(graph_object)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
