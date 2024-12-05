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
    # add one to work-around 0 based indexing without making the code
    # to complicated
    before_mtx = np.zeros(shape=(max_page+1, max_page+1), dtype=int)
    for i, j in ord_rules:
        before_mtx[i, j] = -1  # i is before j, so i is "less" then j
        before_mtx[j, i] = 1  # j is after i, so j is "greater" then i


    if part == 1:
        for up in updates:
            # order the list based on be 'before' relation
            ups = sorted(up, key=functools.cmp_to_key(lambda i, j: before_mtx[i, j]))
            if ups == up:
                mid = up[len(up) // 2]  # get the middle element of lists that are in the correct order
                result += mid
    else:
        # part 2
        for up in updates:
            # order the list based on be 'before' relation
            ups = sorted(up, key=functools.cmp_to_key(lambda i, j: before_mtx[i, j]))
            if ups != up:
                mid = ups[len(up) // 2]  # get the middle element of the SORTED list that are NOT in the correct order
                result += mid

    return result


if __name__ == "__main__":
    result = main(lines, args.part)
    print(f"{script_name} D{day_number:02} input file {args.filename} part {args.part} result: {result}")