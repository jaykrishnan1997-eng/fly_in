#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   main.py                                              :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/03 14:17:07 by jkrishna            #+#    #+#            #
#   Updated: 2026/08/03 14:23:39 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import sys


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage is: python3 main.py <path/to/map.txt>")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Unknown error: {e}")
