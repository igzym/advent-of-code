import sys
import re
import util

DAY = "03"


def read_schematic(lines):
    schematic = []
    for line in lines:
        schematic.append(line)
        print(line)
    return schematic


def char_at(schematic, i, j):
    if i < 0 or i >= len(schematic):
        return None
    if j < 0 or j >= len(schematic[i]):
        return None
    return schematic[i][j]


def is_symbol(schematic, i, j):
    c = char_at(schematic, i, j)
    if c is None or c == ".":
        return False
    if ord(c) >= ord("0") and ord(c) <= ord("9"):
        # it's a digit, not a symbol
        return False
    return True


def is_next_to_symbol(schematic, i, j):
    b = False
    b = b or is_symbol(schematic, i - 1, j - 1)
    b = b or is_symbol(schematic, i - 1, j)
    b = b or is_symbol(schematic, i - 1, j + 1)
    b = b or is_symbol(schematic, i, j - 1)
    b = b or is_symbol(schematic, i, j + 1)
    b = b or is_symbol(schematic, i + 1, j - 1)
    b = b or is_symbol(schematic, i + 1, j)
    b = b or is_symbol(schematic, i + 1, j + 1)
    return b


def part_1_solution(lines):
    schematic = read_schematic(lines)

    answer = 0

    i = 0
    for row in schematic:
        # find all numbers and their locations
        numbers = []
        num_start_idx = []
        ss = 0  # start of search
        while True:
            m = re.search(r"[0-9]+", row[ss:])
            if not m:
                break
            b, e = m.span()
            match = m.string[b:e]
            numbers.append(match)
            num_start_idx.append(ss + b)
            ss += e  # start next search after the last match
        print(f"row {row}", i, numbers, num_start_idx)
        # now check the surroundings of each number
        for ni in range(len(numbers)):
            n = numbers[ni]
            idx = num_start_idx[ni]
            is_part_number = False
            for j in range(idx, idx + len(n)):
                if is_next_to_symbol(schematic, i, j):
                    is_part_number = True
                    break
            if is_part_number:
                print("...", n, "is a part number")
                answer += int(n)
        i += 1
    return answer


def part_2_solution(lines):
    for line in lines:
        pass
    raise RuntimeError(f"part {part} not implemented")


# ===== part below doesn't change =====


def main(input_file, part):
    lines = util.read_lines(input_file)

    if part == 1:
        answer = part_1_solution(lines)
    else:
        answer = part_2_solution(lines)

    print(f"D{DAY} part {part} answer:", answer)


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
