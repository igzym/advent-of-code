import os
import util
import re
import functools
import numpy as np

from util import debug

script_name = os.path.basename(__file__)
day_number = 5

args = util.parse_args(script_name, day_number)

print(args.filename, args.part)

lines = util.read_lines(args.filename)


def main(lines, part):
    result = 0

    ord_rules_l, updates_l = util.split_lines_on_blank_line(lines)

    debug("===")
    ord_rules = [list(map(int, util.split_re(lne, "\|"))) for lne in ord_rules_l]
    debug(ord_rules)
    debug("===")
    updates = [list(map(int, util.split_re(lne, ","))) for lne in updates_l]
    debug(updates)

    # determine highest page number
    max_page = 0
    for up in updates:
        max_page = max(max_page, max(up))
    debug("max_page", max_page)

    # create a matrix representing "before" relation between pages
    #
    # add an extra row and column which will be ignored, this will allow
    # simpler 'notation' using 1-based insted of the usual 0-based indexing
    #
    # for larger problem sizes made a lot more efficient by allocating only
    # the range of [min_page, max_page] elements with appropriate shift in usage
    #
    # using a sparse instead of a dense matrix would most likely be justified
    #
    # this matrix will then be used to implement a comparison function
    # for sorting the elements in the 'updates' list
    before_mtx = np.zeros(shape=(max_page+1, max_page+1), dtype=int)
    for i, j in ord_rules:
        before_mtx[i, j] = -1  # i is before j, so i is "less" then j
        before_mtx[j, i] = 1  # j is after i, so j is "greater" then i


    # surrogate key implementation for sorting
    class K(object):
        def __init__(self, page):
            self.page = page
        def __lt__(self, other):
            return before_mtx[self.page, other.page] < 0


    if part == 1:
        for up in updates:
            # order the list based on 'before' relation
            ups = sorted(up, key=K)
            if ups == up:
                # middle element of lists that are in the correct order
                mid = up[len(up) // 2]
                result += mid
    else:
        # part 2
        for up in updates:
            # order the list based on 'before' relation
            ups = sorted(up, key=K)
            if ups != up:
                # middle element of lists that are NOT in the correct order, AFTER sorting
                mid = ups[len(up) // 2]
                result += mid

    return result


if __name__ == "__main__":
    result = main(lines, args.part)
    print(f"{script_name} D{day_number:02} input file {args.filename} part {args.part} result: {result}")
