import sys
import re
from collections import defaultdict

import util

DAY = "05"


def parse_map_declaration(line):
    x = (line.split()[0]).split("-")
    src = x[0]
    dst = x[2]
    return src, dst


class Range:
    def __init__(self, dst_start: int, src_start: int, length: int):
        self.dst_start = dst_start
        self.dst_end = dst_start + length - 1
        self.src_start = src_start
        self.src_end = src_start + length - 1

    def __str__(self):
        return f"{self.src_start}-{self.src_end} -> {self.dst_start}-{self.dst_end}"

    def __repr__(self):
        return str(self)

    def map(self, src: int):
        if self.src_start <= src and src <= self.src_end:
            return self.dst_start + (src - self.src_start)
        else:
            return None  # no map possible via this range

    def map_range(self, rs, re):
        m_rs = self.map(rs)
        m_re = self.map(re)

        # print(f"| map_range {rs} {re} -> {m_rs}, {m_re}")

        output_ranges = []

        if m_rs is None and m_re is None:
            # none of the input point range limits are inside the map
            if re < self.src_start or rs > self.src_end:
                # completely outside of the map's input range
                # identity transformation
                output_ranges.append((rs, re))
            else:
                # input range encompasses the map's input range
                output_ranges.append(
                    (rs, self.src_start - 1)
                )  # part smaller than map input range
                output_ranges.append((self.dst_start, self.dst_end))  # the map itself
                output_ranges.append(
                    (self.src_end + 1, re)
                )  # the part larger than the map input range
        elif m_re is None:
            # only the start point is actually shifted by the map
            # we split into two intervals - one shifted by map one identity
            output_ranges.append((m_rs, self.dst_end))  # shifted by map
            output_ranges.append((self.src_end + 1, re))  # identity
        elif m_rs is None:
            # only the end point is actually shifted by the map
            # we split into two intervals - one identity and one shifted by map
            output_ranges.append((rs, self.src_start - 1))  # identity
            output_ranges.append((self.dst_start, m_re))  # shifted by map
        else:
            # input range wholy contained in mapping range
            output_ranges.append((m_rs, m_re))

        return output_ranges


class Map:
    def __init__(self, src: str, dst: str):
        self.src = src
        self.dst = dst
        self.ranges: list[Range] = []

    def add_range(self, rnge: Range):
        # keep ranges sorted in increasing range of source
        inserted = False
        for i in range(len(self.ranges)):
            ernge = self.ranges[i]
            if ernge.src_start >= rnge.src_start:
                self.ranges.insert(i, rnge)
                inserted = True
                break
        if not inserted:
            self.ranges.append(rnge)

    def dump(self):
        print(f"| map: {self.src} -> {self.dst}")
        for rnge in self.ranges:
            print(f"|    {rnge}")

    def __str__(self):
        from pprint import pformat

        s = f"map: {self.src} -> {self.dst}"
        rr = [pformat(rnge) for rnge in self.ranges]
        return s + " " + ", ".join(rr)

    def __repr__(self):
        return str(self)

    def map(self, src):
        dst = None
        for rnge in self.ranges:
            dst = rnge.map(src)
            if dst is not None:
                break

        if dst is None:
            # no mapping range found
            dst = src

        return dst


def parse_input(lines):
    seeds = None
    map_ranges = dict()  # src: ranges for mapping src to dest
    curmap = None
    src = dst = None

    for line in lines:
        if line.startswith("seeds:"):
            seeds = [int(s) for s in line.split()[1:]]
        elif line.endswith("map:"):
            if curmap is not None:
                map_ranges[src] = curmap
                # curmap.dump()
            src, dst = parse_map_declaration(line)
            curmap = Map(src, dst)
            # print("| map", src, "->", dst)
        elif re.match(r"\d", line):  # starts with a digit
            ds, ss, length = [int(v) for v in line.split()]
            rnge = Range(ds, ss, length)
            # print(f"| got {rnge}")
            curmap.add_range(rnge)
    if curmap is not None:
        map_ranges[src] = curmap
        # curmap.dump()

    return seeds, map_ranges


def part_1_solution(lines):
    seeds, map_ranges = parse_input(lines)

    from pprint import pformat

    # print("| seeds", seeds)
    # print("| map_ranges", pformat(map_ranges))

    location = []
    for seed in seeds:
        src = "seed"
        dst = None
        src_value = seed
        while dst != "location":
            map_rnge = map_ranges[src]
            dst = map_rnge.dst
            dst_value = map_rnge.map(src_value)
            # print(f"| seed {seed} found link {src} -> {dst}, val: {src_value} -> {dst_value}")
            src = dst
            src_value = dst_value
        # print(f"| seed {seed} {dst} {dst_value}")
        location.append(dst_value)
    return min(location)


def part_2_solution(lines):
    seeds_raw, map_ranges = parse_input(lines)
    # convert list of seeds to a list of seed ranges
    seeds = []
    for i in range(0, len(seeds_raw), 2):
        b = seeds_raw[i]
        n = seeds_raw[i + 1]
        e = b + n - 1
        seeds.append([b, e])

    from pprint import pformat

    print(f"| seed {seeds}")

    # just for fun, map seed through the maps
    ss, se = seeds[0]
    src = "seed"
    map_rnge = map_ranges[src]
    dst = map_rnge.dst

    x = ss
    for ernge in map_rnge.ranges:
        d = ernge.map(x)


def run_unit_tests():
    unit_test("test_input.txt", 1, 35)
    unit_test("input.txt", 1, 424490994)
    unit_test("test_input.txt", 2, 46)


# ===== part below doesn't change =====


def main(input_file, part):
    lines = util.read_lines(input_file)

    if part == 1:
        answer = part_1_solution(lines)
    else:
        answer = part_2_solution(lines)

    print(f"D{DAY} part {part} answer:", answer)


def unit_test(input_file, part, expected):
    print("unit test:", input_file, part, expected)
    lines = util.read_lines(input_file)

    if part == 1:
        answer = part_1_solution(lines)
    else:
        answer = part_2_solution(lines)

    assert answer == expected, f"expected: {expected} != actual: {answer}"


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"usage: python {sys.argv[0]} INPUT_FILE_NAME PART_NO")
        sys.exit(1)

    input_file = sys.argv[1]
    part = sys.argv[2]
    if part not in ["1", "2"]:
        print(f"invalid part value '{sys.argv[2]}' must be '1' or '2'")
        sys.exit(1)
    part = int(part)
    main(input_file, part)
