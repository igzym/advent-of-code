import sys
import re

input_file = sys.argv[1]

with open(input_file) as f:
    lines = [line.rstrip() for line in f.readlines()]

answer = 0  # it will be a sum of two digit number composed of first and last digit in each line

for line in lines:
    # find the first digit
    first_digit = None
    for x in range(len(line)):
        if re.search('[0-9]', line[x]):
            first_digit = int(line[x])
            break
    # find the last digit
    last_digit = None
    for x in reversed(range(len(line))):
        if re.search('[0-9]', line[x]):
            last_digit = int(line[x])
            break
    # print(line, first_digit, last_digit)

    # update result
    answer += first_digit * 10 + last_digit

print('D01 Q1 answer:', answer)
