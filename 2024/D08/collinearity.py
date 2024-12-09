import os
import util
import numpy as np
from collections import defaultdict
import copy
from typing import Tuple, List, Set, Optional  # need to upgrade python to 3.12 for modern typing syntax

from util import debug

script_name = os.path.basename(__file__)
day_number = 8

args = util.parse_args(script_name, day_number)

print(args.filename, args.part)

lines = util.read_lines(args.filename)


Position = Tuple[int, int]
Pair = Tuple[Position, Position]


def pairs(seq: List[Position]) -> List[Pair]:
    """all distinct pairs of elements of seq"""
    # a recursive solution
    # if seq lenght is one return empty result
    # otherwise return pairs of first element with every other element
    # and add the same starting at the second element
    if len(seq) < 2:
        return []
    r = [(seq[0], s) for s in seq[1:]]
    r += pairs(seq[1:])
    return r


def antinodes(pair: Pair, mtx, k) -> List[Position]:
    """for given pair of positions, return the list of antinodes
    there fall on the line determined by the pair of positons
    at distance exactly k times the segment determined by the pair
    k can be 0
    retain only values that are on the grid"""
    m, n = mtx.shape

    p1, p2 = pair

    x1, y1 = p1
    x2, y2 = p2


    a1: Position = x2 + k*(x2 - x1), y2 + k*(y2 - y1)  # add k times delta p2 - p1
    a2: Position = x1 - k*(x2 - x1), y1 - k*(y2 - y1)  # subtract k times delta p2 - p1

    def in_grid(p: Position) -> bool:
        x, y = p
        if x < 0 or x >= m:
            return False
        if y < 0 or y >= n:
            return False
        return True
    a = []
    if in_grid(a1):
        a.append(a1)
    if in_grid(a2):
        a.append(a2)
    return a

def print_map(label, lm, an=None):
    lmc = copy.deepcopy(lm)
    if an is not None:
        for a in an:
            i, j= a
            lmc[i][j] = '#'
    debug(label)
    for r in lmc:
        debug(''.join(r))

def main(lines, part):
    result = 0

    # convert input into a list of lists of characters
    # representing the grid
    lines_mtx = util.to_matrix(lines)
    #debug(lines_mtx)
    # now convert this into a numpy array
    mtx = np.array(lines_mtx)
    debug(mtx)

    debug("map dimensions", mtx.shape)
    print_map("map", lines_mtx)

    # identify different frequencies on the grid
    # represnted by different letters (case-sensitive) or numbers
    # and their positions
    freqs = defaultdict(list)
    m, n = mtx.shape
    for i in range(m):
        for j in range(n):
            f = mtx[i, j]
            if f == '.':  # skip empty spaces
                continue
            freqs[f].append((i, j))
    debug("freqs")
    for f, pos in freqs.items():
        debug("f", f, "pos", pos)

    # go through the positons of each frequency and generate all
    # unique pairs of their positions

    pospd = dict()
    debug("pairs")
    for f, pos in freqs.items():
        posp = pairs(pos)
        pospd[f] = posp
        debug("f", f, "pos", pos)
        debug("... pos pairs", posp)

    unique_an = set()
    print_map("initial", lines_mtx)
    for f, posp in pospd.items():
        for p in posp:
            if part == 1:
                # just look for a single pair of antidotes
                # at a fixed distance
                an = antinodes(p, mtx, 1)
            else:
                # look for antinodes at an increasing distance
                # starting from 0 which means the position of the generating pair
                # of antennas, until neither of the generated antinodes falls on
                # the grid
                k = 0
                an = []
                while True:
                    an0 = antinodes(p, mtx, k)  # antinodes at distance k
                    debug("colinearity for", p, "with k", k, "gives", an0)
                    if not an0:  # non of them are on the grid we can stop trying to extend the distance
                        break
                    an.extend(an0)
                    k += 1
            print_map(f"with antinodes for {f} at {p}: {an}", lines_mtx, an)
            for a in an:
                unique_an.add(a)
    debug("result", len(unique_an))
    print_map("final antinodes", lines_mtx, list(unique_an))

    result = len(unique_an)
    return result


if __name__ == "__main__":
    result = main(lines, args.part)
    print(f"{script_name} D{day_number:02} input file {args.filename} part {args.part} result: {result}")
