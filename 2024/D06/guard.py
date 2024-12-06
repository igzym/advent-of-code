import os
import util
import numpy as np

from util import debug

script_name = os.path.basename(__file__)
day_number = 5

args = util.parse_args(script_name, day_number)

print(args.filename, args.part)

lines = util.read_lines(args.filename)


UP = "^"
DOWN = "v"
LEFT = "<"
RIGHT = ">"

# directions in the order of turing to the right
guard_dir_cycle = [UP, RIGHT, DOWN, LEFT]

def initialize(lines):
    lines_mtx = util.to_matrix(lines)
    nrows = len(lines_mtx)
    ncols = len(lines_mtx[0])

    mapm = np.zeros(shape=(nrows, ncols), dtype=int)
    guard_i, guard_j = None, None
    guard_dir = None
    guard_j = None
    for i in range(nrows):
        for j in range(ncols):
            c = lines_mtx[i][j]
            if c == "#":
                mapm[i, j] = 1  # obstacle position
            elif c in guard_dir_cycle:
                guard_i, guard_j = i, j  # guard position
                guard_dir = c
    state = [guard_i, guard_j, guard_dir]
    return mapm, state


def next_pos(state):
    # calculate next position assuming you are NOT falling off the edge
    i, j, d = state
    if d == UP:
        i -=1
    elif d == DOWN:
        i += 1
    elif d == LEFT:
        j -= 1
    elif d == RIGHT:
        j += 1
    return i, j


def legal_pos(mapm, i, j):
    # does given position contain an obstacle?
    return mapm[i, j] == 0

def turn(mapm, state):
    # change direction by turning to right
    i, j, d = state
    gsi = guard_dir_cycle.index(d)
    d = guard_dir_cycle[(gsi + 1) % len(guard_dir_cycle)]
    state[2] = d

def about_to_exit(mapm, state):
    # am I on the edge of the map and facing the direction
    # such that next move would leave the map?
    i, j, d = state
    m, n = mapm.shape
    if d == UP and i == 0:
        return True
    if d == DOWN and i == m - 1:
        return True
    if d == LEFT and j == 0:
        return True
    if d == RIGHT and j == n - 1:
        return True
    return False


def move(mapm, state):
    # change the state, either change the position if possibe
    # or turn
    ni, nj = next_pos(state)
    if legal_pos(mapm, ni, nj):
        state[0], state[1] = ni, nj
    else:
        turn(mapm, state)


def main(lines, part):
    result = 0

    if not lines:
        raise RuntimeError("empty input")

    mapm, state = initialize(lines)
            
    debug(mapm)
    debug("guard state", state)

    visited = set()

    if part == 1:
        while True:
            debug(result, "in state", state)
            i, j = state[:2]
            if (i, j) not in visited:
                result += 1
                debug(result, "newly visited", state)
                visited.add((i, j))  # mark current location as being visited
            if about_to_exit(mapm, state):
                # next move, the guard will exit, stop iterating
                debug(result, "exiting", state)
                break
            # generate next move
            move(mapm, state)
    else:
        pass

    return result


if __name__ == "__main__":
    result = main(lines, args.part)
    print(f"{script_name} D{day_number:02} input file {args.filename} part {args.part} result: {result}")
