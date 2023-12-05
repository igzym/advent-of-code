import sys
import re

DAY = "02"


def split_re(text, sep):
    """split using given separator ignoring any white space around it"""
    return re.split(r"\s*" + sep + r"\s*", text)


def parse_game_line(line):
    """parse input line that looks like this:
    Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    """
    game_id_txt, game_txt = split_re(line, ":")
    _, game_id = split_re(game_id_txt, " ")
    game_id = int(game_id)
    draws_txt_lst = split_re(game_txt, ";")

    game = []
    for d in draws_txt_lst:
        cube_set_t = re.split(r"\s*,\s*", d)  # ['3 blue', '4 red']
        draw = {}
        for cs_t in cube_set_t:
            count, colour = re.split(r"\s+", cs_t)  # ['3', 'blue']
            count = int(count)
            draw[colour] = count
        game.append(draw)
    return game_id, game


def max_game_size(game, colour):
    """max number of cube of given colour seen in any draw of the given game"""
    max_size = 0
    for d in game:
        size = d.get(colour, 0)
        if size > max_size:
            max_size = size
    return max_size


COLOURS = ["red", "green", "blue"]


def power_of_game(game):
    """product of minimum number of cubes of each colour that must have been present
    in the bag for a game to be possible
    it's the product of max counts of cubes per colour for all draws

    this is required for the part 2 of the problem
    """
    min_col = {c: 0 for c in COLOURS}
    for d in game:
        for c, n in d.items():
            cur_min = min_col.get(c)
            if n >= cur_min:
                min_col[c] = n
    power = 1
    for _, n in min_col.items():
        power *= n
    return power


def part_1_solution(lines):
    possible_game_ids = set()
    for line in lines:
        game_id, game = parse_game_line(line)
        # only 12 red cubes, 13 green cubes, and 14 blue cubes
        possible = True
        for max_size, colour in [(12, "red"), (13, "green"), (14, "blue")]:
            if max_size < max_game_size(game, colour):
                possible = False
                break
        if possible:
            possible_game_ids.add(game_id)
    # print(possible_game_ids)
    return sum(possible_game_ids)


def part_2_solution(lines):
    answer = 0
    for line in lines:
        game_id, game = parse_game_line(line)
        answer += power_of_game(game)
    return answer


def main(input_file, part=1):
    with open(input_file) as f:
        lines = [line.rstrip() for line in f.readlines()]

    if part == 1:
        answer = part_1_solution(lines)
    else:
        answer = part_2_solution(lines)

    print(f"D{DAY} part{part} answer:", answer)


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
