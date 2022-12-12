from __future__ import annotations

import sys

import re

sys.argv.pop(0)  # get rid of first argument - script name
input_file = sys.argv.pop(0)

with open(input_file) as f:
    lines = f.readlines()

def height_code_to_num(heightcode: str) -> int:
    if heightcode == 'S':
        # special case for starting node
        return height_code_to_num('a')
    if heightcode == 'E':
        # special case for ending node
        return height_code_to_num('z')

    ohc = ord(heightcode)
    if ohc >= ord('a') and ohc <= ord('z'):
        return ohc - ord('a')
    if ohc >= ord('A') and ohc <= ord('Z'):
        return ohc - ord('A') + ord('z')

class Node:
    row: int
    col: int
    height: int
    neighbor_coords: set
    neighbors: list[Node]
    start: bool = False
    target: bool = False
    explored: bool = False

    def __init__(self, row: int, col: int, height: int) -> None:
        self.row, self.col = row, col  # position in grid
        self.height = height
        self.neighbor_coords = set()
        self.neighbors = []
        self.parent = None  # parent node if in shortest path
    
    def addNeighbor(self, nnode: Node) -> None:
        if nnode.height - self.height <= 1:
            # allow movement to higher elevation only if at most one step
            # all other elevation changes are authorized
            ncoord = (nnode.row, nnode.col)
            # prevent duplicate addition
            if ncoord not in self.neighbor_coords:
                self.neighbor_coords.add(ncoord)
                self.neighbors.append(nnode)
                # print(f"dbg {self} added neighbor {nnode}")
    
    def setStart(self) -> None:
        self.start = True

    def setTarget(self) -> None:
        self.target = True

    def __str__(self) -> str:
        special = ""
        if self.start:
            special = " (S)"
        elif self.target:
            special = " (E)"
        return f"({self.row}, {self.col}) h: {self.height}{special}"

# row, col position of start and end nodes
start_node = (None, None)
target_node = (None, None)

nodegrid = dict()

nrow = len(lines)
ncol = len(lines[0].strip())
print('nrow', nrow, 'ncol', ncol)

currow = 0
for ll in lines:
    rowline = ll.strip()
    curcol = 0
    for c in rowline:
        nd = Node(currow, curcol, height_code_to_num(c))
        nodegrid[(currow, curcol)] = nd
        if c == 'S':
            start_node = (currow, curcol)
            nd.setStart()
        if c == 'E':
            target_node = (currow, curcol)
            nd.setTarget()
        curcol += 1
    currow += 1


def attach_neighbours(nd: Node) -> None:
    LEFT = (0, -1)
    RIGHT = (0, 1)
    UP = (-1, 0)
    DOWN = (1, 0)

    row, col = nd.row, nd.col
    for drow, dcol in LEFT, RIGHT, UP, DOWN:
        new_row = row + drow
        new_col = col + dcol

        if new_row < 0 or new_row >= nrow:
            continue
        if new_col < 0 or new_col >= ncol:
            continue

        nd.addNeighbor(nodegrid[(new_row, new_col)])

for row in range(nrow):
    for col in range(ncol):
        attach_neighbours(nodegrid[(row, col)])

visited_node = set()
def show_graph(nd: Node) -> None:
    if (nd.row, nd.col) in visited_node:
        return
    visited_node.add((nd.row, nd.col))
    print(f"[ node {nd} has {len(nd.neighbor_coords)} nbrs")
    nbs = ", ".join( [f"({nn})" for nn in nd.neighbors] )
    print(f"   Nbrs: {nbs} ]")
    for nn in nd.neighbors:
        show_graph(nn)

# show_graph(nodegrid[(0, 0)])

# print(nrow, ncol)
# print(len(visited_node))
# print(len(nodegrid))


# reset fields used during BFS to their initial values
def reset_for_BFS():
    for r in range(nrow):
        for c in range(ncol):
            nd: Node = nodegrid[(r, c)]
            nd.explored = False
            nd.parent = None

# adapted from https://en.wikipedia.org/wiki/Breadth-first_search
def BFS(root: Node):
    ctrl_cnt = 0
    Q = [] # queue
    root.explored = True
    Q.append(root)
    while len(Q) > 0:
        v: Node = Q.pop(0)
        # print(f"popped node {v}, len(Q) {len(Q)}")
        if v.target:
            return v
        for w in v.neighbors:
            if not w.explored:
                w.explored = True
                w.parent = v
                Q.append(w)
                ctrl_cnt += 1

# run after BFS, with g being BFS result
def get_path(g):
    path = []
    while g is not None:
        path.append(g)
        g = g.parent
    return path

# part 1 do a breadth-first search starting at S
root = nodegrid[start_node]
g = BFS(root)
print("BFS goal", g)

path = get_path(g)

# print([str(n) for n in path], len(path))

print(f"RESULT: part 1: shortest path length from S: {len(path)-1}")

# part 2 - shortest of all paths starting at 'a'
paths = []
for r in range(nrow):
    for c in range(ncol):
        nd: Node = nodegrid[(r, c)]
        if nd.height == 0: # ie, 'a'
            reset_for_BFS()
            g = BFS(nd)
            if g is not None:
                path = get_path(g)
                # print(f" path: {[str(p) for p in path]}")
                paths.append(path)

spaths = sorted(paths, key=lambda p: len(p))

print(f"RESULT: part 2: shortest path length from any 'a': {len(spaths[0])-1}")
