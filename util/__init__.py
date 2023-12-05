import re


def read_lines(input_file):
    """read lines from a file and return as a list, stripping
    trailing newlines"""
    with open(input_file) as f:
        lines = [line.rstrip() for line in f.readlines()]
    return lines


def split_re(text, sep):
    """split using given separator ignoring any white space around it"""
    return re.split(r"\s*" + sep + r"\s*", text)
