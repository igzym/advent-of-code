import re
import argparse


DEBUG = False


def debug(*args, **kwargs):
    global DEBUG
    if DEBUG:
        print("DEBUG", *args, **kwargs)


def split_lines_on_blank_line(lines):
    line_set = []
    cur_lines = []
    for lne in lines:
        if lne == "":
            line_set.append(cur_lines)
            cur_lines = []
        else:
            cur_lines.append(lne)
    if cur_lines:
        line_set.append(cur_lines)
    return line_set


def read_lines(input_file):
    """read lines from a file and return as a list, stripping
    trailing newlines"""
    with open(input_file) as f:
        lines = [line.rstrip() for line in f.readlines()]
    return lines


def split_re(text, sep):
    """split using given separator ignoring any white space around it"""
    return re.split(r"\s*" + sep + r"\s*", text)


def parse_args(script_name, day_number):
    global DEBUG
    parser = argparse.ArgumentParser(
                        prog=f"python {script_name}",
                        description=f"Solution to advent of code D{day_number:02} problem",
                        )

    parser.add_argument('filename')
    parser.add_argument('-d', '--debug', help='turn on debugging', action='store_true')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-p', '--part', help='part number', type=int, choices=[1, 2], required=True)

    args = parser.parse_args()
    DEBUG = args.debug
    return args
