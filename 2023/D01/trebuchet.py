import sys
import re

input_file = sys.argv[1]
part = 1
if len(sys.argv) > 2:
    part = int(sys.argv[2])

digits = [str(x) for x in range(10)]
digit_words = ['zero', 'one', 'two', 'three', 'four',
               'five', 'six', 'seven', 'eight', 'nine']
# numeric value of digit expressed as a word
digit_word_val = {dw: d for dw, d in zip(digit_words, digits)}

def find_first_digit(text: str):
    """Look for first digit either as digit, or as word
    return a two digit number obained by concatenating the first and last digit"""
    first_digit_pos = len(text) + 1
    last_digit_pos = -1
    first_digit_val = last_digit_vale = None
    # look for digits as digits - go through all 10 digits
    for d in digits:
        r = text.find(d)
        # is it more to the left than any one previously found?
        if r >= 0 and r < first_digit_pos:
            first_digit_pos = r
            first_digit_val = d
        r = text.rfind(d)
        # is it more to the right than any one previously found?
        if r >= 0 and r > last_digit_pos:
            last_digit_pos = r
            last_digit_val = d
    # look for digits as words - go through all 10 digits
    for dw in digit_words:
        r = text.find(dw)
        # is it more to the left than any one previously found?
        if r >= 0 and r < first_digit_pos:
            first_digit_pos = r
            first_digit_val = digit_word_val[dw]
        r = text.rfind(dw)
        # is it more to the right than any one previously found?
        if r >= 0 and r > last_digit_pos:
            last_digit_pos = r
            last_digit_val = digit_word_val[dw]
    return int(first_digit_val + last_digit_val)

def main(input_file, part=1):
    with open(input_file) as f:
        lines = [line.rstrip() for line in f.readlines()]

    answer = 0  # it will be a sum of two digit number composed of first and last digit in each line

    for line in lines:
        if part == 1:
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
        elif part == 2:
            answer += find_first_digit(line)

    print(f'D01 part{part} answer:', answer)

if __name__ == "__main__":
    main(input_file, part)