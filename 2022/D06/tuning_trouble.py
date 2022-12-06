import sys

import re

input_file = sys.argv[1]

with open(input_file) as f:
    lines = f.readlines()

assert len(lines) == 1

last_4_chars = []

# I have only one line of input, but keep loop structure
# for further puzzles
for ll in lines:
    input_stream = list(ll.strip("\n"))

assert len(input_stream) >= 4

def all_different(chars):
    return len(set(chars)) == len(chars)

# initialize
last_4_chars = input_stream[:4]
for next_char_in_stream_idx in range(4, len(input_stream)):
    next_char = input_stream[next_char_in_stream_idx]
    chars_read = next_char_in_stream_idx
    # print(f"DEBUG next_char {next_char} chars_read {chars_read} last_4_chars {last_4_chars}")
    if all_different(last_4_chars):
        print(f"RESULT: {next_char_in_stream_idx}")
        break
    last_4_chars.pop(0)
    last_4_chars.append(next_char)
