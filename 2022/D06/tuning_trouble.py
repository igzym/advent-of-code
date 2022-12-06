import sys

import re

assert len(sys.argv) >= 3, "not enough command line arguments"
input_file = sys.argv[1]
min_unique = int(sys.argv[2])

with open(input_file) as f:
    lines = f.readlines()

assert len(lines) == 1

last_n_chars = []

# I have only one line of input, but keep loop structure
# for further puzzles
for ll in lines:
    input_stream = list(ll.strip("\n"))

assert len(input_stream) >= min_unique

def all_different(chars):
    return len(set(chars)) == len(chars)

# initialize
last_n_chargs = input_stream[:min_unique]
for next_char_in_stream_idx in range(min_unique, len(input_stream)):
    next_char = input_stream[next_char_in_stream_idx]
    chars_read = next_char_in_stream_idx
    # print(f"DEBUG next_char {next_char} chars_read {chars_read} last_n_chargs {last_n_chargs}")
    if all_different(last_n_chargs):
        print(f"RESULT: {next_char_in_stream_idx}")
        break
    last_n_chargs.pop(0)
    last_n_chargs.append(next_char)
