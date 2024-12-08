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


def op_subsets(n, ops):
    # generate all possible variations of length n the operations in 'ops'
    # if M is the number of operations (len(ops))
    # then generate M^n numbers, converted to base=M representation
    # then convert each digit into an operation
    base = len(ops)
    def to_base(i, base, w):
        s = np.base_repr(i, base)
        s = "0" * (w - len(s)) + s  # pad to left with zeros to fixed width
        return s
    def replace_digits(x):
        for d in range(base):
            x = x.replace(str(d), ops[d])
        return x
    subsets = [to_base(i, base, n) for i in range(pow(base, n))]
    return [[d for d in replace_digits(s)] for s in subsets]

def main(lines, part):
    result = 0

    # do the parsing via list comprexension
    # not the easiest to read but quick to write
    # we first split on ': ' to separate the expected result and the list of values on which to compute
    # then we split the values to compute in a list
    # we convert all to int
    inp = [(int(ex), list(map(int, elt.split(' ')))) for (ex, elt) in [lne.split(': ') for lne in lines]]
    for x in inp:
        debug(x)

    for expval, args in inp:
        debug(expval, args)
        n = len(args)
        if part == 1:
            ops_sets = op_subsets(n - 1, ['+', '*'])
        else:
            # part 2
            ops_sets = op_subsets(n - 1, ['+', '*', '|'])
        for ops in ops_sets:
            debug(ops)
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
                elif e == '|':
                    operation = lambda a, b: int(str(a) + str(b))
                else:
                    r = operation(r, e)
            if r == expval:
                result += r
                break

    return result


if __name__ == "__main__":
    result = main(lines, args.part)
    print(f"{script_name} D{day_number:02} input file {args.filename} part {args.part} result: {result}")
