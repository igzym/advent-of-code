import os
import util
import re
import functools

from util import debug

script_name = os.path.basename(__file__)
day_number = 3

args = util.parse_args(script_name, day_number)

print(args.filename, args.part)

lines = util.read_lines(args.filename)

pat_mul = re.compile(r"mul\((\d+),(\d+)\)")
pat_do = re.compile(r"do\(\)")
pat_dont = re.compile(r"don't\(\)")

def match_pat(txt, pat):
    """return positon after first matched pattern
    or -1 if not found"""
    pos_after = -1
    r = pat.search(txt)
    if r:
        pos_after = r.span()[1]
    return pos_after


match_do = functools.partial(match_pat, pat=pat_do)
match_dont = functools.partial(match_pat, pat=pat_dont)


def match_mul(txt):
    """return result of mul(A,B), A*B, and the pointer to the first
    character after the matched mul. Returns None, -1 if no match found"""
    #print("DEBUG, match_next on", txt)
    r = pat_mul.search(txt)
    if r:
        A = int(r.group(1))
        B = int(r.group(2))
        char_after = r.span()[1]
        return A*B, char_after
    return None, -1


def main(lines, part):
    result = 0

    if part == 1:
        for line in lines:
            txt = line
            while True:
                r, char_after = match_mul(txt)
                if r is None:
                    break
                result += r
                txt = txt[char_after:]
    else:
        # part 2
        enabled = True
        for line in lines:
            txt = line
            while True:
                posvec = []
                pos = match_do(txt)
                if pos >= 0:
                    posvec.append((pos, "do"))
                pos = match_dont(txt)
                if pos >= 0:
                    posvec.append((pos, "dont"))
                r, pos = match_mul(txt)
                if pos >= 0:
                    posvec.append((pos, "mul"))

                if len(posvec) == 0:
                    break

                debug("txt", txt)
                debug("posvec", posvec)
                debug("sorted(posvec)", sorted(posvec))

                # take the first matching token
                pos, kind = sorted(posvec, key=lambda e: e[0])[0]
                #print("DEBUG", pos, kind)
                last_pos = pos
                if kind == "dont":
                    enabled = False
                    debug("Disable")
                elif kind == "do":
                    enabled = True
                    debug("Enable")
                else:  # mul
                    if enabled:
                        debug("adding product", r)
                        result += r

                txt = txt[last_pos:]
 
    return result


if __name__ == "__main__":
    result = main(lines, args.part)
    print(f"{script_name} D{day_number:02} input file {args.filename} part {args.part} result: {result}")
