# -*- coding: utf-8 -*-

import os
import sys

MIN_PYTHON_VERSION = (3, 7)

if sys.version_info < MIN_PYTHON_VERSION:
    print("This script '{}' requires Python version 3.7 or newer".format(__file__))
    sys.exit(1)

from _path_ascii_remover import remove_non_ascii_text_from

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('You need to provide path(s) to change as program arguments')
        exit(1)
    remove_non_ascii_text_from(sys.argv[1:])