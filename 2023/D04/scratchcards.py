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
        cards.append((cid, win, have))
    return cards


def matches(cid, win, have):
    nmatch = 0
    for h in have:
        if h in win:
            nmatch += 1
    return nmatch


def part_1_solution(lines):
    cards = read_cards(lines)
    # from pprint import pprint
    # pprint(lines)
    # pprint(cards)

    points = 0
    for cid, win, have in cards:
        nmatch = matches(cid, win, have)
        if nmatch > 0:
            points += 2 ** (nmatch - 1)

    return points


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


g_CARDS = None  # for debugging


def dbg_card_status():
    return ", ".join([f"{c.cid}: {c.get_copies():2}" for c in g_CARDS])


def generate_copies(cards):
    if len(cards) == 0:
        return
    tcard = cards[0]
    m = tcard.value()
    for card in cards[1 : m + 1]:
        card.add_copies(tcard.get_copies())
    # print(f"| after processing top card: {tcard.cid} v: {m}, copied {list(range(1+1,m+1+1))}")
    # print(f"| {dbg_card_status()}")
    generate_copies(cards[1:])


def part_2_solution(lines):
    global g_CARDS
    g_CARDS = []
    cards = g_CARDS

    raw_cards = read_cards(lines)
    for cid, win, have in raw_cards:
        cards.append(Card(cid, win, have))

    # print(f"| initial state")
    # print(f"| {dbg_card_status()}")
    generate_copies(cards)

    return sum([card.get_copies() for card in cards])


def run_unit_tests():
    unit_test("test_input.txt", 1, 13)
    unit_test("input.txt", 1, 19855)
    unit_test("test_input.txt", 2, 30)
    unit_test("input.txt", 2, 10378710)
    unit_test("example_input.txt", 2, 7)


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
