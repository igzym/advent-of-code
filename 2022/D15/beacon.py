from __future__ import annotations

import sys
import re
import json

sys.argv.pop(0)  # get rid of first argument - script name

if not sys.argv:
    print("usage: FILE_NAME Y_LINE_TO_TEST [COORD_MIN-COORD_MAX")
    sys.exit(1)

input_file = sys.argv.pop(0)
y_line_to_test = int(sys.argv.pop(0))

coord_range_str = "0-4000000"
if sys.argv:
    coord_range_str = sys.argv.pop(0)

coord_range = [int(x) for x in coord_range_str.split("-")]
print("coord_range", coord_range)

with open(input_file) as f:
    lines = f.readlines()

class Beacon:
    x: int
    y: int
    def __init__(self, x:int, y:int) -> None:
        self.x = x
        self.y = y

    def loc(self):
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

    def loc(self):
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

x_min = y_min = 10**9
x_max = y_max = -10**9

for loc, sensor in sensors.items():
    x_min = min(x_min, sensor.x, sensor.beacon.x)
    y_min = min(y_min, sensor.y, sensor.beacon.y)
    x_max = max(x_max, sensor.x, sensor.beacon.x)
    y_max = max(y_max, sensor.y, sensor.beacon.y)

print(f"x range: [{x_min}, {x_max}], y range: [{y_min}, {y_max}]")

# now we see if we need to extend de grid to include the full exclusion
# zones for all sensors
# this was not clearly stated in the spec and I only figured it out
# by looking at the diagrams
# without this change the result is too low, but with it it's correct
# in the test case the result is correct in both cases, which is unfortunate
for loc, sensor in sensors.items():
    x_min = min(x_min, sensor.x - sensor.dist())
    y_min = min(y_min, sensor.y - sensor.dist())
    x_max = max(x_max, sensor.x + sensor.dist())
    y_max = max(y_max, sensor.y + sensor.dist())

print ("after including all exclusion zones")
print(f"x range: [{x_min}, {x_max}], y range: [{y_min}, {y_max}]")

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

# print_grid()

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
        remd = None
        ints = []
    else:
        # than go left and right the remaining distance
        remd = d - dist_s_l  # >= because of above check
        x_s = sensor.x - remd
        x_e = sensor.x + remd
        # clip to grid limits
        x_s = max(x_min, x_s)
        x_e = min(x_max, x_e)

        ints = [x_s, x_e]

    # print(f"sensor loc: {loc},  d: {sensor.dist()}")
    # print(f"    dist_s_l: {dist_s_l}), remd: {remd}: {ints}")

    return ints

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


# part 1 puzzle - count points where a beacon cannot occur in one specific horizontal line
def excluded_positions(y, exclude_known_beacons=True, exc_intervals=None):
    n_excluded = 0
    inters_set = []  # sortd list of disjoint intervals of interection of the line at y with
                    # the 'exlusion zones' of all the sensors
    # print(f"line: {y}")
    for loc, sensor in sensors.items():
        ints = intersection_line_sensor(y, sensor)
        dtl = abs(sensor.y - y)
        if len(ints) > 0:  # if intersection not empty add it
            inters_set = add_to_intersection_set(inters_set, ints)
        # print(f".. ints = {ints}, new inters_set = {inters_set}")

    for ints in inters_set:
        xs, xe = ints
        n_excluded += xe - xs + 1  # number of points in the intersection interval
        # now remove any beacons that (related to other sensors) that may on the same line
        if exclude_known_beacons:
            # this is the part 1 behaviour
            beacons_excluded = set()
            for loc, sensor in sensors.items():
                bloc = sensor.beacon.loc()
                if bloc in beacons_excluded:
                    continue
                bx, by = bloc
                if by == y and xs <= bx and bx <= xe:
                    n_excluded -= 1
                    beacons_excluded.add(bloc)
                    # print(f"excluded beacon at {bloc}")
    if exc_intervals is not None:
        exc_intervals.append(inters_set)
    return n_excluded

n_excluded = excluded_positions(y_line_to_test)

print(f"RESULT: part 1: n_excluded in line {y_line_to_test} = {n_excluded}")
print(f"dbg: part 1: there are {xdim} total positions")
print(f"dbg: part 1: places where beacon may occur: {xdim - n_excluded}")

# part 2 - locate the only position that can contain a beacon
x_min, x_max = coord_range
y_min, y_max = coord_range
xdim = x_max - x_min + 1
ydim = y_max - y_min + 1
inters_set = []
y = y_min
ctrl_print = 0
for y in range(y_min, y_max + 1):
    inters_set_c = []
    n_excluded = excluded_positions(y, exclude_known_beacons=False, exc_intervals=inters_set_c)
    inters_set = inters_set_c[0]  # value returned by the above function
    # print(f"dbg: y {y} n_excluded {n_excluded}, xdim {xdim}, inters_set {inters_set_c[0]}")
    rem_spots = xdim - n_excluded
    if rem_spots == 1:
        print("Found the spot:", inters_set, y)
        break  # we can break here because the spec guarantees only one such line exists
    if ctrl_print == 0:
        print(f"dbg control print at y {y} (inters_set len: {len(inters_set)}, rem_spots: {rem_spots}")
    ctrl_print = (ctrl_print + 1)%100000

# if the spot is at the start or at the beginning of the line
# we'll have only one interval in inters_set
assert len(inters_set) > 0
x_result = 0
if len(inters_set) == 1:
    xi_s, xi_e = inters_set[0]
    if xi_s > x_min:
        x_result = x_min
    else:
        assert xi_e < x_max
        x_result = x_max
else:
    # otherwise we have exactly two intervals, and the
    # sought position is just in the middle of them
    assert len(inters_set) == 2
    int1, int2 = inters_set
    xe1 = int1[1]
    xs2 = int2[0]
    assert xs2 - xe1 == 2
    x_result = xe1 + 1 # or, xs2 - 1
tuning_frequency = x_result * 4000000 + y
print(f"RESULT part 2: beacon is at {x_result}, {y}, tuning_frequency: {tuning_frequency}")