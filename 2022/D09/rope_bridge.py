import sys

import re

input_file = sys.argv[1]

with open(input_file) as f:
    lines = f.readlines()

moves = []

knot_pos = [ [0, 0] for _ in range(10) ]

unique_tail_pos = set()

from math import sqrt
sqr2 = sqrt(2)

def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0

# update position of knot i based on state of previous knot, i-1
def update_knot_pos(knot_pos, i):
    global unique_tail_pos

    head = knot_pos[i]
    tail = knot_pos[i-1]

    rvec = [x - y for x, y in zip(head, tail)]

    rvec_hor, rvec_ver = rvec[0], rvec[1]

    rvec_mod = sqrt(rvec_hor**2 + rvec_ver**2) 

    # print(f"DEBUG head {head_pos} tail {tail_pos} rvec_hor, rvec_ver {rvec_hor, rvec_ver} rvec_mod {rvec_mod}")

    if rvec_mod -  sqr2 > 0.001:
        # not touching, need to move the tail
        tail[0] += sign(rvec_hor)
        tail[1] += sign(rvec_ver)

    # print(f"DEBUG ... after move tail {tail_pos}")

    if i-1 == 0:
        # this is the tail of the entire rope
        unique_tail_pos.add(tuple(tail))

for ll in lines:
    ll = ll.strip("\n")
    direction, size = ll.split()
    size = int(size)

    moves.append([direction, size])

def move_vector(direction):
    if direction == 'L':
        return [-1, 0]
    elif direction == 'R':
        return [1, 0]
    elif direction == 'U':
        return [0, 1]
    elif direction == 'D':
        return [0, -1]
    else:
        assert False, f"Unexpected direction {direction!r}"

head_pos = knot_pos[-1]

for direction, size in moves:
    # print(f"DEBUG move {direction, size}")
    move_vec = move_vector(direction)
    for _ in range(size):
        # make the move incrementally
        # update head
        head_pos[0] += move_vec[0]
        head_pos[1] += move_vec[1]
        # propagate to nodes previous to it
        for kidx in list(range(len(knot_pos)-1, 0, -1)):
            update_knot_pos(knot_pos, kidx)

print(f"RESULT part 1: {len(unique_tail_pos)} unique tail locations")
