import sys

import re

input_file = sys.argv[1]

with open(input_file) as f:
    lines = f.readlines()

tree_mtx = []

for ll in lines:
    ll = ll.strip("\n")
    # print(f"DEBUG {ll}")

    tree_mtx.append([])

    for col in ll:
        tree_mtx[-1].append(int(col))

# print(tree_mtx)

M = len(tree_mtx)
N = len(tree_mtx[0])

def visible(tree_mtx, i, j):
    if i == 0 or j == 0:
        # print(f"DEBUG visible {i},{j} (left or upper edge)")
        return True
    if i == M-1 or j == N-1:
        # print(f"DEBUG visible {i},{j} (right or bottom edge)")
        return True

    visible = False

    # scan row (j dimension) to the 'left'
    max_h = 0
    for jj in range(0, j):
        if tree_mtx[i][jj] > max_h:
            max_h = tree_mtx[i][jj]
    if max_h < tree_mtx[i][j]:
        return True

    # scan row (j dimension) to the 'right'
    max_h = 0
    for jj in range(j+1, N):
        if tree_mtx[i][jj] > max_h:
            max_h = tree_mtx[i][jj]
    if max_h < tree_mtx[i][j]:
        return True

    # scan column (i dimension) from 'above'
    max_h = 0
    for ii in range(0, i):
        if tree_mtx[ii][j] > max_h:
            max_h = tree_mtx[ii][j]
    if max_h < tree_mtx[i][j]:
        return True

    # scan column (i dimension) from 'below'
    max_h = 0
    for ii in range(i+1, M):
        if tree_mtx[ii][j] > max_h:
            max_h = tree_mtx[ii][j]
    if max_h < tree_mtx[i][j]:
        return True

    return False

def scenic_score(tree_mtx, i, j):
    sc_score = 1

    my_h = tree_mtx[i][j]

    # scan row (j dimension) to the 'left'
    score_d = 0
    for jj in range(j-1, -1, -1):
        score_d += 1
        if my_h <= tree_mtx[i][jj]:
            break
    sc_score *= score_d

    # scan row (j dimension) to the 'right'
    score_d = 0
    for jj in range(j+1, N):
        score_d += 1
        if my_h <= tree_mtx[i][jj]:
            break
    sc_score *= score_d

    # scan colum (i dimension) towards the 'top'
    score_d = 0
    for ii in range(i-1, -1, -1):
        score_d += 1
        if my_h <= tree_mtx[ii][j]:
            break
    sc_score *= score_d

    # scan colum (i dimension) towards the 'bottom'
    score_d = 0
    for ii in range(i+1, M):
        score_d += 1
        if my_h <= tree_mtx[ii][j]:
            break
    sc_score *= score_d

    return sc_score

n_visible = 0
max_sc_score = 0
for i in range(M):
    for j in range(N):
        if visible(tree_mtx, i, j):
            n_visible += 1
        sc_score = scenic_score(tree_mtx, i, j)
        max_sc_score = max(max_sc_score, sc_score)

print(f"RESULT: n_visible {n_visible}")
print(f"RESULT: max_sc_score {max_sc_score}")
