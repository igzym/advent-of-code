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

# print("list pairs:")
# for lpi in range(len(list_pairs)):
#     lp = list_pairs[lpi]
#     print(f"{lpi+1}: {str(lp[0]):35} : {str(lp[1]):35}")

def list_compare(a, b):
    """return negative value if a < b, 0 if a == b, positive value if a > b"""
    # print(f"... compare input a = {a}, b = {b}")
    
    for i in range(min(len(a), len(b))):

        aa = a[i]
        bb = b[i]

        # print(f"... ... comparing {aa} and {bb}")
        
        if type(aa) == int and type(bb) == int:
            if aa > bb:
                # print(f"... ... {aa} > {bb}")
                return 1
            if aa < bb:
                # print(f"... ... {aa} < {bb}")
                return -1
            # print(f"... ... {aa} = {bb}")
        else:
            # both are lists, or mixed type
            if type(aa) == int:
                aa = [ aa ]
            if type(bb) == int:
                bb = [ bb ]
            r = list_compare(aa, bb)
            if r > 0:
                pass # print(f"... ... {aa} > {bb}")
            elif r < 0:
                pass # print(f"... ... {aa} < {bb}")
            else:
                pass # print(f"... ... {aa} = {bb}")
            if r != 0:
                return r
    return len(a) - len(b)

tot_lpi = 0  # sum of indexes of pairs in right order: part 1 answer
for lpi in range(len(list_pairs)):
    lp = list_pairs[lpi]
    a, b = lp[0], lp[1]
    # print(f"============ pair index {lpi+1} {a} vs {b}")
    r = list_compare(a, b)
    rs = "right order" if r else "NOT right order"
    if r <= 0:
        # print(f"{a} <= {b} right order")
        tot_lpi += (lpi+1)
    else:
        pass # print(f"{a} > {b} NOT right order")
    # print(f"   pair index {lpi+1} {rs}")

print(f"RESULT part 1: tot_lpi {tot_lpi}")

packets = []
for pp in list_pairs:
    packets.append(pp[0])
    packets.append(pp[1])
divider_packets = [[[2]], [[6]]]

packets += divider_packets

import functools

packets_s = sorted(packets, key=functools.cmp_to_key(list_compare))

pidx = 1
decode_key = 1
for p in packets_s:
    # print(pidx, p)
    if p in divider_packets:
        decode_key *= pidx
    pidx += 1

print(f"RESULT part 2: decode key: {decode_key}")

