import sys

import re

input_file = sys.argv[1]

with open(input_file) as f:
    lines = f.readlines()

moves = []

head_pos = [0, 0]
tail_pos = [0, 0]

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


def update_tail_pos(head_pos, tail_pos):
    global unique_tail_pos

    rvec = [x - y for x, y in zip(head_pos, tail_pos)]

    rvec_hor, rvec_ver = rvec[0], rvec[1]

    rvec_mod = sqrt(rvec_hor**2 + rvec_ver**2) 

    # print(f"DEBUG head {head_pos} tail {tail_pos} rvec_hor, rvec_ver {rvec_hor, rvec_ver} rvec_mod {rvec_mod}")

    if rvec_mod -  sqr2 > 0.001:
        # not touching, need to move the tail
        tail_pos[0] += sign(rvec_hor)
        tail_pos[1] += sign(rvec_ver)

    # print(f"DEBUG ... after move tail {tail_pos}")


    unique_tail_pos.add(tuple(tail_pos))

for ll in lines:
    ll = ll.strip("\n")
    direction, size = ll.split()
    size = int(size)

    moves.append([direction, size])

for direction, size in moves:
    # print(f"DEBUG move {direction, size}")
    if direction == 'L':
        for m in range(size):
            head_pos[0] -= 1
            update_tail_pos(head_pos, tail_pos)
    elif direction == 'R':
        for m in range(size):
            head_pos[0] += 1
            update_tail_pos(head_pos, tail_pos)
    elif direction == 'U':
        for m in range(size):
            head_pos[1] += 1
            update_tail_pos(head_pos, tail_pos)
    elif direction == 'D':
        for m in range(size):
            head_pos[1] -= 1
            update_tail_pos(head_pos, tail_pos)
    else:
        assert False, f"unexpected direction {direction}"

print(f"RESULT part 1: {len(unique_tail_pos)} unique tail locations")
