import os
import util

script_name = os.path.basename(__file__)
day_number = 2

args = util.parse_args(script_name, day_number)

print(args.filename, args.part)

lines = util.read_lines(args.filename)


def sign(x):
    if x < 0:
        return -1
    elif x == 0:
        return 0
    else:
        return 1

def is_safe(levels):
    delta_sign_sum = 0  # sum of signs of the deltas between consecutive levels
    unsafe_level_change = False
    for i in range(0, len(levels) - 1):
        delta = levels[i + 1] - levels[i]
        if abs(delta) < 1 or abs(delta) > 3:
            unsafe_level_change = True
            break 
        delta_sign_sum += sign(delta)

    if unsafe_level_change:
        return False
    
    if abs(delta_sign_sum) != len(levels) - 1:
        # change signs were not monotonic
        return False
    
    return True


def is_safe_after_dampening(levels):
    if is_safe(levels):
        return True
    # try removing elements one by one and checking again
    for i in range(len(levels)):
        dampened_levels = list(levels)
        dampened_levels.pop(i)
        if is_safe(dampened_levels):
            return True
    return False


def main(lines, part):
    # convert input to lists of integers
    values = [list(map(int, x.split())) for x in lines]
    result = 0

    if part == 1:
        for levels in values:
            if is_safe(levels):
                result += 1
    else:
        # part 2
        for levels in values:
            if is_safe_after_dampening(levels):
                result += 1

    return result


if __name__ == "__main__":
    result = main(lines, args.part)
    print(f"{script_name} D{day_number:02} input file {args.filename} part {args.part} result: {result}")