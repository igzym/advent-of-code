from __future__ import annotations

import sys
import re
import json

sys.argv.pop(0)  # get rid of first argument - script name
input_file = sys.argv.pop(0)

with open(input_file) as f:
    lines = f.readlines()

list_pairs = []

current_pair = []
for ll in lines:
    ll = ll.strip()
    if ll == "":
        list_pairs.append(current_pair)
        current_pair = []
    else:
        current_pair.append(json.loads(ll))

list_pairs.append(current_pair)  # the last one is not delimited by a blank line

import pprint

# print("list pairs:")
# for lpi in range(len(list_pairs)):
#     lp = list_pairs[lpi]
#     print(f"{lpi+1}: {str(lp[0]):35} : {str(lp[1]):35}")

def list_compare(a, b):
    # return True if list a is 'smaller' than b
    if len(a) > 0 and len(b) == 0:
        return False  # a is non-empty and b is empty, so a is not smaller
    if len(a) == 0:
        return True  # a is empty and cannot be bigger than b
    if len(b) == 0:
        return False  # b is empty and a is not, a is not smaller

    # both a and b are non-empty
    assert len(a) > 0
    assert len(b) > 0

    if type(a[0]) == int and type(b[0]) == int:
        if a[0] > b[0]:
            return False
        return list_compare(a[1:], b[1:])

    if type(a[0]) == int:
        atoc = [ a[0] ]
    else:
        atoc = a[0]
    
    if type(b[0]) == int:
        btoc = [ b[0] ]
    else:
        btoc = b[0]
    
    return list_compare(atoc, btoc)


tot_lpi = 0  # sum of indexes of pairs in right order: part 1 answer
for lpi in range(len(list_pairs)):
    lp = list_pairs[lpi]
    a, b = lp[0], lp[1]
    print(f"pair index {lpi+1}")
    if list_compare(a, b):
        print(f"{a} <= {b}")
        tot_lpi += (lpi+1)
    else:
        print(f"{a} > {b}")

print(f"RESULT part 1: tot_lpi {tot_lpi}")

