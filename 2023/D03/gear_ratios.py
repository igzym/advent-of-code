import sys
import re
import util

DAY = "03"

GEAR_SYMBOL = "*"


def read_schematic(lines):
    schematic = []
    for line in lines:
        schematic.append(line)
        # print(line)
    return schematic


def char_at(schematic, i, j):
    if i < 0 or i >= len(schematic):
        return None
    if j < 0 or j >= len(schematic[i]):
        return None
    return schematic[i][j]


def is_symbol(c):
    if c is None or c == ".":
        return False
    if ord(c) >= ord("0") and ord(c) <= ord("9"):
        # it's a digit, not a symbol
        return False
    return True


def is_next_to_symbol(schematic, i: int, j: int, gears: set[tuple[int, int]] = None):
    """return True if there are any adjacent symbols to cell (i, j)
    if a set is provided in gears argument add coordinates of GEAR symbols found"""
    surroundings = [
        (i - 1, j - 1),
        (i - 1, j),
        (i - 1, j + 1),
        (i, j - 1),
        (i, j + 1),
        (i + 1, j - 1),
        (i + 1, j),
        (i + 1, j + 1),
    ]

    b = False
    for ii, jj in surroundings:
        c = char_at(schematic, ii, jj)
        b = b or is_symbol(c)
        if c == GEAR_SYMBOL and gears is not None:
            gears.add((ii, jj))
    return b


def find_all_numbers(row):
    # find all numbers and their locations
    numbers = []
    num_spans = []
    ss = 0  # start of search
    while True:
        m = re.search(r"[0-9]+", row[ss:])
        if not m:
            break
        b, e = m.span()
        match = m.string[b:e]
        numbers.append(match)
        num_spans.append((ss + b, ss + b + e - 1))
        ss += e  # start next search after the last match
    # print(f"row {row}", i, numbers, num_spans)
    return numbers, num_spans


def find_part_numbers_and_gears(schematic):
    i = 0
    numbers = []
    part_number_status: list[list[bool]] = []
    adjacent_gears = []
    for row in schematic:
        # find all numbers and their locations
        r_numbers, num_spans = find_all_numbers(row)
        r_part_number_status: list[bool] = []
        r_adjacent_gears = []
        # now check the surroundings of each number
        for ni in range(len(r_numbers)):
            n = r_numbers[ni]
            idx = num_spans[ni][0]  # start of number
            is_part_number = False
            gears = set()
            for j in range(idx, idx + len(n)):
                if is_next_to_symbol(schematic, i, j, gears):
                    is_part_number = True
            r_part_number_status.append(is_part_number)
            r_adjacent_gears.append(gears)
        numbers.append(r_numbers)
        part_number_status.append(r_part_number_status)
        adjacent_gears.append(r_adjacent_gears)
        i += 1
    # from pprint import pprint
    # print('schematic')
    # pprint(schematic)
    # print('numbers')
    # pprint(numbers)
    # print('part_number_status')
    # pprint(part_number_status)
    # print('adjacent_gears')
    # pprint(adjacent_gears)
    return numbers, part_number_status, adjacent_gears


def part_1_solution(lines):
    schematic = read_schematic(lines)

    numbers, part_number_status, adjacent_gears = find_part_numbers_and_gears(schematic)

    answer = 0

    for i in range(len(numbers)):
        for ni in range(len(numbers[i])):
            if part_number_status[i][ni]:
                answer += int(numbers[i][ni])

    return answer


def part_2_solution(lines):
    for line in lines:
        pass
    raise RuntimeError(f"part {part} not implemented")


def run_unit_tests():
    unit_test("input.txt", 1, 556057)


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
