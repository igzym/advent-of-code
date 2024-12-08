import os
import util
import numpy as np
from collections import defaultdict
import operator
from typing import Tuple, List, Set, Optional  # need to upgrade python to 3.12 for modern typing syntax

from util import debug

script_name = os.path.basename(__file__)
day_number = 7

args = util.parse_args(script_name, day_number)

print(args.filename, args.part)

lines = util.read_lines(args.filename)

def op_subsets(n):
    subs_bin = [format(i, f'0{n}b') for i in range(pow(2, n))]
    return [[o for o in s.replace('0', '+').replace('1', '*')] for s in subs_bin]



def main(lines, part):
    result = 0

    inp = [(int(ex), list(map(int, elt.split(' ')))) for (ex, elt) in [lne.split(': ') for lne in lines]]

    if part == 1:
        for expval, args in inp:
            debug(expval, args)
            n = len(args)
            ops_sets = op_subsets(n - 1)
            for ops in ops_sets:
                expr = [None] * (len(ops) + len(args))
                for i in range(len(args) - 1):
                    expr[i*2] = args[i]
                    expr[i*2+1] = ops[i]
                expr[-1] = args[-1]
                debug("...", expr)
                r = expr[0]
                f = None
                for e in expr[1:]:
                    debug("... ...", repr(e), f)
                    if e == '+':
                        f = operator.add
                    elif e == '*':
                        f = operator.mul
                    else:
                        r = f(r, e)
                if r == expval:
                    result += r
                    break
    else:
        # part 2
        pass

    return result


if __name__ == "__main__":
    result = main(lines, args.part)
    print(f"{script_name} D{day_number:02} input file {args.filename} part {args.part} result: {result}")
