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
    # using binary numbers to generate a set of possible variations of
    # two values (+ or *) over n positions
    # for example, if n = 3 then we generate binary numbers
    # 000, 001, 010, 011, 100, 101, 110, 111
    # which correspond to (if 0 -> '+' and 1 -> '*')
    # a + b + c + d, a + b + c * d, ..., a * b * c * d
    subs_bin = [format(i, f'0{n}b') for i in range(pow(2, n))]
    return [[o for o in s.replace('0', '+').replace('1', '*')] for s in subs_bin]


def main(lines, part):
    result = 0

    # do the parsing via list comprexension
    # not the easiest to read but quick to write
    # we first split on ': ' to separate the expected result and the list of values on which to compute
    # then we split the values to compute in a list
    # we convert all to int
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
                # calculate the expressions for each of the combination of the
                # operators and check agains the expected (test) value
                # for each one that matches add to the overall result
                r = expr[0]
                operation = None
                for e in expr[1:]:
                    debug("... ...", repr(e), operation)
                    if e == '+':
                        operation = operator.add
                    elif e == '*':
                        operation = operator.mul
                    else:
                        r = operation(r, e)
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
