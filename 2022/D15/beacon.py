from __future__ import annotations

import sys
import re
import json

sys.argv.pop(0)  # get rid of first argument - script name

if not sys.argv:
    print("usage: FILE_NAME Y_LINE_TO_TEST")
    sys.exit(1)

input_file = sys.argv.pop(0)
y_line_to_test = int(sys.argv.pop(0))

part = "part2" # choose behaviour - part 1 or part 2 of the puzzle
if sys.argv:
    part = sys.argv.pop(0)

assert part in ["part1", "part2"], f"unexpected part={part}"

with open(input_file) as f:
    lines = f.readlines()

class Beacon:
    x: int
    y: int
    def __init__(self, x:int, y:int) -> None:
        self.x = x
        self.y = y

    def loc(self) -> tuple(int):
        return (self.x, self.y)

class Sensor:
    x: int
    y: int
    beacon: Beacon
    def __init__(self, x:int, y:int, beacon:Beacon) -> None:
        self.x = x
        self.y = y
        self.beacon = beacon

    def dist(self) -> int:
        return abs(self.x - self.beacon.x) + abs(self.y - self.beacon.y)

    def loc(self) -> tuple(int):
        return (self.x, self.y)

sensors = dict()
beacon_loc = set()

for ll in lines:
    ll = ll.strip()

    m = re.match(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", ll)
    assert m, f"input line not in exected format ({ll})"
    sensor_x, sensor_y = int(m.group(1)), int(m.group(2))
    beacon_x, beacon_y = int(m.group(3)), int(m.group(4))  # beacon closest to sensor

    beacon = Beacon(beacon_x, beacon_y)
    sensor = Sensor(sensor_x, sensor_y, beacon)

    # print(f"S: [{sensor[0]:8}, {sensor[1]:8}], B: [{beacon[0]:8}, {beacon[1]:8}]")

    sensors[sensor.loc()] = sensor
    beacon_loc.add(beacon.loc())

x_min = y_min = 1e30
x_max = y_max = -1e30

for loc, sensor in sensors.items():
    x_min = min(x_min, sensor.x, sensor.beacon.x)
    y_min = min(y_min, sensor.y, sensor.beacon.y)
    x_max = max(x_max, sensor.x, sensor.beacon.x)
    y_max = max(y_max, sensor.y, sensor.beacon.y)

print("x_min", x_min, "y_min", y_min, "x_max", x_max, "y_max", y_max)

xdim = x_max - x_min + 1
ydim = y_max - y_min + 1

# print the grid for experimentation
def print_grid() -> None:
    if xdim > 50 or ydim > 30:
        print(f"grid is to big to be printed ({ydim} x {xdim})")
        return
    for y in range(y_min, y_max + 1):
        dl = ""
        for x in range(x_min, x_max + 1):
            if (x, y) in sensors:
                dl += "S"
            elif (x, y) in beacon_loc:
                dl += "B"
            else:
                dl += "."
        print(dl)

print_grid()

def intersection_line_sensor(y: int, sensor: Sensor):
    # return two points of intersection of the exlusion
    # zone of a sensor with a given horizontal line at
    # coorinate y

    # distance of sensor to its nearest beacon
    d = sensor.dist()

    # vertical distance from sensor to line
    dist_s_l = abs(sensor.y - y)
    if d < dist_s_l:
        # line is too far from sensor, no intersection
        return []

    # than go left and right the remaining distance
    remd = d - dist_s_l  # >= because of above check
    x_s = sensor.x - remd
    x_e = sensor.x + remd
    # clip to grid limits
    x_s = max(x_min, x_s)
    x_e = min(x_max, x_e)

    return [x_s, x_e]

# adapted from D04 - camp cleanup

def merge_intervals_if_possible(a, b):
    maxmin = max(a[0], b[0])
    minmax = min(a[1], b[1])
    if maxmin <= minmax: # they intersect on [maxmin, minmax]
        # single merged interval
        return [ [min(a[0], b[0]), max(a[1], b[1]) ] ]
    else:
        return [a, b]

def add_to_intersection_set(inters_set, new_inters):
    # add interval to a set of disjoint intervals, merging intervals if possible

    if len(new_inters) == 0:
        return list(inters_set)
    if len(inters_set) == 0:
        return [ new_inters ]

    curr_inters = inters_set[0]
    m_ints = merge_intervals_if_possible(curr_inters, new_inters)
    if len(m_ints) > 1:  # could not merge
        if new_inters[1] < curr_inters[0]:
            # new one is all the way to the left, insert at start and we are done
            return [ new_inters] + inters_set
        # otherwise try to merge with some of the subsequent ones
        return [ curr_inters ] + add_to_intersection_set(inters_set[1:], new_inters)

    # merged with the head interval in list
    # throw away the current head interval and try continue
    # trying to merge with the rest of the list
    new_inters = m_ints[0]  # it's the only one
    return add_to_intersection_set(inters_set[1:], new_inters)


y = y_line_to_test
n_excluded = 0
inters_set = []  # sortd list of disjoint intervals of interection of the line at y with
                 # the 'exlusion zones' of all the sensors
for loc, sensor in sensors.items():
    ints = intersection_line_sensor(y, sensor)
    dtl = abs(sensor.y - y)
    print(f"sensor at loc {loc}, with d {sensor.dist()}, inters. with line at {y} (at dist {dtl}): {ints}")
    if len(ints) > 0:  # if intersection not empty add it
        inters_set = add_to_intersection_set(inters_set, ints)
    print(f".. ints = {ints}, new inters_set = {inters_set}")

for ints in inters_set:
    xs, xe = ints
    n_excluded += xe - xs + 1  # number of points in the intersection interval
    # now remove any beacons that (related to other sensors) that may on the same line
    beacons_excluded = set()
    for loc, sensor in sensors.items():
        bloc = sensor.beacon.loc()
        if bloc in beacons_excluded:
            continue
        bx, by = bloc
        if by == y and xs <= bx and bx <= xe:
            n_excluded -= 1
            beacons_excluded.add(bloc)
            print(f"excluded beacon at {bloc}")

print(f"RESULT: n_excluded in line {y} = {n_excluded}")
