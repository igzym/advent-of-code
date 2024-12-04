import os
import util
import re
import functools

from util import debug

script_name = os.path.basename(__file__)
day_number = 4

args = util.parse_args(script_name, day_number)

print(args.filename, args.part)

lines = util.read_lines(args.filename)

# we have a matrix of letters like the one below
# XMAS..
# M..X..
# XMAS..
# S.....
# count occurrences of XMAS and SAMX, horizontally, vertically
# AND diagonally
# in this example we have 2 horizontal and 1 vertical, total of 3

# method: use string search by line:
# - original matrix: horizontal direction
# - transposed matrix: vertical direction
# - skewed right and transposed - right to left top to bottom diagonal direction
#   after skew the diagonal becomes vertical, transpose makes it horizontal
# - skewed left and transposed - left to right top to bottom diagonal direction
#   after skew the diagonal becomes vertical, transpose makes it horizontal

def print_matrix(label, lines):
    debug(label)
    debug('=======')
    for l in lines:
        debug(l)


def to_matrix(lines):
    matrix = [[c for c in line] for line in lines]
    return matrix



def transpose_matrix(lines):
    # build a transpose of the input matrix
    # XMXS
    # M.M.
    # A.A.
    # XSX.
    # etc...

    if not lines:
        raise RuntimeError("input data is empty")

    nrows = len(lines)
    ncols = len(lines[0])

    matrix = to_matrix(lines)

    tr_lines = []
    for c in range(ncols):
        tr_r = ""
        for r in range(nrows):
            tr_r += matrix[r][c]
        tr_lines.append(tr_r)

    return tr_lines


def skew_matrix(lines, direction):
    """Transform matrix
    ABCD
    EFGH
    IJKL

    into

    direction > 0       direction < 0
    skew right          skew left
    ABCD..               ..ABCD
    .EFGH.               .EFGH.
    ..IJKL               IJKL..
    """

    if not lines:
        raise RuntimeError("input data is empty")
    
    if direction == 0:
        raise RuntimeError("direction cannot be 0")

    sk_lines = []
    i = 0
    nrows = len(lines)
    for r in lines:
        if direction > 0:
            nr = "."*i + r + "."*(nrows-1-i)
        elif direction < 0:
            nr = "."*(nrows-1-i) + r +  "."*i
        sk_lines.append(nr)
        i += 1

    return sk_lines


def count(lines):
    cnt = 0
    for r in lines:
        cnt += r.count("XMAS")
        cnt += r.count("SAMX")
    debug(cnt)
    return cnt


def match_xmas_pattern_in_matrix(matrix, r0, c0):
    """does upper left corner of matrix match
    M.M
    .A.
    S.S
    where M and S can be swapped along diagonal
    """

    d1 = False
    d2 = False

    def mtx(r, c):
        return matrix[r0 + r][c0 + c]

    if mtx(1, 1) == 'A':
        if mtx(0, 0) == 'M' and mtx(2, 2) == 'S':
            d1 = True
        elif mtx(0, 0) == 'S' and mtx(2, 2) == 'M':
            d1 = True
        if mtx(0, 2) == 'M' and mtx(2, 0) == 'S':
            d2 = True
        elif mtx(0, 2) == 'S' and mtx(2, 0) == 'M':
            d2 = True

    return d1 and d2


def main(lines, part):
    result = 0

    tr_lines = transpose_matrix(lines)
    sk_lines_r = transpose_matrix(skew_matrix(lines, +1))
    sk_lines_l = transpose_matrix(skew_matrix(lines, -1))

    print_matrix("lines", lines)
    print_matrix("tr_lines", tr_lines)
    print_matrix("sk_lines_r", sk_lines_r)
    print_matrix("sk_lines_l", sk_lines_l)

    if part == 1:
        result += count(lines)
        result += count(tr_lines)
        result += count(sk_lines_l)
        result += count(sk_lines_r)
    else:
        # part 2
        matrix = to_matrix(lines)
        if len(matrix) == 0:
            raise RuntimeError("empty input")
        nrows = len(matrix)
        ncols = len(matrix[0])
        for i in range(nrows - 2):
            for j in range(ncols - 2):
                if match_xmas_pattern_in_matrix(matrix, i, j):
                    result += 1

    return result


if __name__ == "__main__":
    result = main(lines, args.part)
    print(f"{script_name} D{day_number:02} input file {args.filename} part {args.part} result: {result}")
