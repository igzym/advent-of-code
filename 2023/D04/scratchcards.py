import sys
import re
import util
from collections import defaultdict

DAY = "04"


def read_cards(lines):
    cards = []
    for line in lines:
        m = re.search(r"Card\s+(\d+): ([0-9 ]*) \| ([0-9 ]*)", line)
        cid = int(m.group(1))
        win = [int(n) for n in m.group(2).split()]
        have = [int(n) for n in m.group(3).split()]
        cards.append(
            [(cid, win, have)]
        )  # each card 'id' can hold a list of cards (in part 2)
    return cards


def part_1_solution(lines):
    cards = read_cards(lines)
    # from pprint import pprint
    # pprint(lines)
    # pprint(cards)

    points = 0
    for clist in cards:
        cid, win, have = clist[0]  # we have exactly one element here in part 2
        nmatch = 0
        for h in have:
            if h in win:
                nmatch += 1
        if nmatch > 0:
            points += 2 ** (nmatch - 1)

    return points


def part_2_solution(lines):
    pass


def run_unit_tests():
    unit_test("test_input.txt", 1, 13)
    unit_test("input.txt", 1, 19855)
    unit_test("test_input.txt", 2, 30)


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
