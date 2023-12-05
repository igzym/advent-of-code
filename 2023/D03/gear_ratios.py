import sys

DAY = "03"


def parse_game_line(line):
    pass


def part_1_solution(lines):
    for line in lines:
        pass
    raise RuntimeError(f"part {part} not implemented")


def part_2_solution(lines):
    for line in lines:
        pass
    raise RuntimeError(f"part {part} not implemented")


# ===== part below doesn't change =====


def main(input_file, part=1):
    with open(input_file) as f:
        lines = [line.rstrip() for line in f.readlines()]

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
