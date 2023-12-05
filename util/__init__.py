import re


def split_re(text, sep):
    """split using given separator ignoring any white space around it"""
    return re.split(r"\s*" + sep + r"\s*", text)
