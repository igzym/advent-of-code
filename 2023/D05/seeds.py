import sys
import re
import util
from collections import defaultdict

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


class Map:
    def __init__(self, src: str, dst: str):
        self.src = src
        self.dst = dst
        self.ranges: list[Range] = []

    def add_range(self, rnge: Range):
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
    pass
    return sum([card.get_copies() for card in cards])


def run_unit_tests():
    unit_test("test_input.txt", 1, 35)
    unit_test("input.txt", 1, 424490994)


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
