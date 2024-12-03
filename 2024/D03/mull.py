import os
import util
import re

script_name = os.path.basename(__file__)
day_number = 3

args = util.parse_args(script_name, day_number)

print(args.filename, args.part)

lines = util.read_lines(args.filename)

pat = re.compile(r"mul\((\d+),(\d+)\)")

def match_next(txt):
    """return result of mul(A,B), A*B, and the pointer to the first
    character after the matched mul. Returns None if no match found"""
    #print("DEBUG, match_next on", txt)
    r = pat.search(txt)
    if r:
        A = int(r.group(1))
        B = int(r.group(2))
        char_after = r.span()[1]
        return A*B, char_after
    return None, None

def main(lines, part):
    # convert input to lists of integers
    result = 0

    if part == 1:
        for line in lines:
            txt = line
            while True:
                r, char_after = match_next(txt)
                if r is None:
                    break
                result += r
                txt = txt[char_after:]
    else:
        # part 2
        pass

    return result


if __name__ == "__main__":
    result = main(lines, args.part)
    print(f"{script_name} D{day_number:02} input file {args.filename} part {args.part} result: {result}")
