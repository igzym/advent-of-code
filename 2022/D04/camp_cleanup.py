import sys

input_file = sys.argv[1]

# Answer sought: number of pairs where one interval is fully
# contained in the other
# number of
n_pairs_with_full_cont = 0

def fully_contained(outer, inner):
    """return True if inner is fully cointained in outer"""
    return inner[0] >= outer[0] and inner[1] <= outer[1]

with open(input_file) as f:
    lines = f.readlines()

for ll in lines:
    pair = ll.strip()
    ranges = pair.split(',')
    # print(f"DEBUG pair: {pair} ranges: {ranges}")
    interval = []
    for r in ranges:
        i = [int(x) for x in r.split('-')]
        # print(f"DEBUG ... interval: {i}")
        interval.append(i)
    if fully_contained(interval[0], interval[1]):
        n_pairs_with_full_cont += 1
    elif fully_contained(interval[1], interval[0]):
        n_pairs_with_full_cont += 1
    # print(f"DEBUG: ... ... n_pairs_with_full_cont {n_pairs_with_full_cont}")

print(f"RESULT: n_pairs_with_full_cont {n_pairs_with_full_cont}")
