import os
import util
import numpy as np
from collections import defaultdict
import copy
from typing import Tuple, List, Set, Optional  # need to upgrade python to 3.12 for modern typing syntax

from util import debug

script_name = os.path.basename(__file__)
day_number = 7

args = util.parse_args(script_name, day_number)

print(args.filename, args.part)

lines = util.read_lines(args.filename)


def main(lines, part):
    result = 0

    inp = [(int(ex), list(map(int, elt.split(' ')))) for (ex, elt) in [lne.split(': ') for lne in lines]]
    for x in inp:
        print(x)

    if part == 1:
        pass
    else:
        # part 2
        pass

    return result


if __name__ == "__main__":
    result = main(lines, args.part)
    print(f"{script_name} D{day_number:02} input file {args.filename} part {args.part} result: {result}")
