import re
import argparse


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
    parser = argparse.ArgumentParser(
                        prog=f"python {script_name}",
                        description=f"Solution to advent of code D{day_number:02} problem",
                        )

    parser.add_argument('filename')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-p', '--part', help='part number', type=int, choices=[1, 2], required=True)

    args = parser.parse_args()
    return args
