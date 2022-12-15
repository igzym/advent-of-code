from __future__ import annotations

import sys
import re
import json

sys.argv.pop(0)  # get rid of first argument - script name
input_file = sys.argv.pop(0)

part = "part2" # choose behaviour - part 1 or part 2 of the puzzle
if sys.argv:
    part = sys.argv.pop(0)

assert part in ["part1", "part2"], f"unexpected part={part}"

with open(input_file) as f:
    lines = f.readlines()

rock_paths = []
for ll in lines:
    ll = ll.strip()
    coords = ll.split(" -> ")
    path = []
    for point in coords:
        pt = [int(v) for v in point.split(",")]
        path.append(pt)
    rock_paths.append(path)

class Grid:
    def __init__(self, rock_paths):
        # x is the horizontal axis
        # y is the vertical axis
        self.rock_paths = rock_paths
        self.max_x = 0
        self.min_x = 1e30
        self.max_y = 0
        self.min_y = 1e30
        for rp in self.rock_paths:
            for x, y in rp:
                self.max_x = max(self.max_x, x)
                self.min_x = min(self.min_x, x)
                self.max_y = max(self.max_y, y)
                self.min_y = min(self.min_y, y)

        if part == "part2":
            # add to more lines below, for the floor at botton
            self.max_y += 2
            # add a few more colums to the left an right (but this will be
            # dynamically adjustable)
            self.min_x -= 3
            self.max_x += 3

        print("x range", self.min_x, self.max_x)
        print("y range", self.min_y, self.max_y)

        self.ydim = self.max_y + 1
        self.xdim = self.max_x - self.min_x + 1

        self.grid = []
        empty_row = [ "." for _ in range(self.xdim)]
        print(len(empty_row))
        for y in range(self.ydim):
            self.grid.append(list(empty_row))

        if part == "part2":
            # add the floor at bottom
            rock_paths.append([ [self.min_x, self.max_y], [self.max_x, self.max_y] ])

        for rp in rock_paths:
            prev_x, prev_y = None, None
            # print(rp)
            for x, y in rp:
                # print(f"{prev_x},{prev_y} -> {x},{y}")
                if [prev_x, prev_y] != [None, None]:
                    if x != prev_x:
                        x1, x2 = prev_x, x
                        if x1 > x2:
                            x2, x1 = x1, x2
                        for xx in range(x1, x2 + 1):
                            self.setElement(xx, y, "#")
                    else:
                        y1, y2 = prev_y, y
                        if y1 > y2:
                            y2, y1 = y1, y2
                        for yy in range(y1, y2 + 1):
                            self.setElement(x, yy, "#")
                prev_x, prev_y = x, y
                # self.display()

    def setElement(self, x, y, val):
        # print(f"setting {x},{y} to {val}")
        self.grid[y][x - self.min_x] = val

    def getElement(self, x, y):
        xx = x - self.min_x
        if xx < 0 or xx >= self.xdim:
            return None
        if y < 0 or y >= self.ydim:
            return None
        return self.grid[y][xx]

    def extend_left(self):
        for y in range(self.ydim):
            self.grid[y].insert(0, "." if y < self.max_y else "#")
        self.min_x -= 1
        self.xdim += 1

    def extend_right(self):
        for y in range(self.ydim):
            self.grid[y].append("." if y < self.max_y else "#")
        self.max_x += 1
        self.xdim += 1

    def display(self):
        for r in self.grid:
            print("".join(r))
        print()

g = Grid(rock_paths)
# g.display()

# simulate one unit of sand
def drop_unit(g: Grid):
    cx, cy = [500, 0]
    abyss = False
    while True:
        blocked = True
        if part == "part2":
            if cx == g.min_x:
                g.extend_left()
            if cx == g.max_x:
                g.extend_right()
        for dx, dy in (0, 1), (-1, 1), (1, 1):
            #if g.getElement(cx+dx, cy+dy) is None:
            #    # falls into void
            #    sys.exit(0)
            #    break
            if g.getElement(cx+dx, cy+dy) is None:
                abyss = True
                break
            if g.getElement(cx+dx, cy+dy) == '.':
                cx += dx
                cy += dy
                blocked = False
                break
        if abyss:
            return False # stop sending more sand
        if blocked:
            g.setElement(cx, cy, 'o')
            if part == "part2":
                if cx == 500 and cy == 0:
                    # g.display()
                    print('at source')
                    return False # stop sending more sand
            break
    return True

sand_units = 0
while drop_unit(g):
    sand_units += 1

if part == "part2":
    sand_units += 1  # ???
# g.display()

print(f"RESULT sand_units {sand_units}")