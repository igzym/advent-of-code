import sys
import re
import util
from collections import defaultdict

DAY = "05"


def part_1_solution(lines):
    pass


# keep in case I need a template to create a different class
class Card:
    def __init__(self, cid, win, have):
        self.cid = cid
        self.win = win
        self.have = have
        self.val = matches(cid, win, have)
        self.copies = 1

    def value(self):
        return self.val

    def add_copies(self, n):
        nc = self.copies + n
        self.copies = nc

    def get_copies(self):
        return self.copies


def part_2_solution(lines):
    pass
    return sum([card.get_copies() for card in cards])


def run_unit_tests():
    unit_test("test_input.txt", 1, -1)


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
