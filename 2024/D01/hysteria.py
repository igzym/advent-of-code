import os
import util

from collections import Counter

script_name = os.path.basename(__file__)
day_number = 1

args = util.parse_args(script_name, day_number)

print(args.filename, args.part)

lines = util.read_lines(args.filename)


def main(lines, part):
    # create a list of pairs of integers
    values = [list(map(int, x.split())) for x in lines]
    result = 0

    # convert into two columns, value on the left to the first columns
    # and the other value to the second column
    col1 = [x[0] for x in values]
    col2 = [x[1] for x in values]

    if part == 1:
        # sort those two columns independently
        col1 = sorted(col1)
        col2 = sorted(col2)
        # result is the sum of the differences of the two respective elements
        result = sum([abs(a - b) for (a, b) in zip(col1, col2)])
    else:
        # part 2 - sum of left list elements multiplied by the number of times they
        # appear in the right list

        # count the appearances of values in the second list
        count2 = Counter(col2)

        # add value times count - use .get to succinctly handle values that do not
        # appear in the second list
        result = sum([x * count2.get(x, 0) for x in col1])

    return result


if __name__ == "__main__":
    result = main(lines, args.part)
    print(f"{script_name} D{day_number:02} input file {args.filename} part {args.part} result: {result}")