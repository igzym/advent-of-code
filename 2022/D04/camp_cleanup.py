import sys

input_file = sys.argv[1]

# part 1 answer sought: number of pairs where one interval is fully
# contained in the other
n_pairs_with_full_cont = 0
# part 2 answer sought: number of pairs with any overlap at all
n_pairs_with_overlap = 0

def fully_contained(outer, inner):
    """return True if inner is fully cointained in outer"""
    return inner[0] >= outer[0] and inner[1] <= outer[1]

def have_overlap(a, b):
    """return True if a and b overlap"""
    # make first interval always be 'on the left', ie
    # have smaller or equal lower bound
    if a[0] > b[0]:
        a, b = b, a
    maxmin = max(a[0], b[0])
    minmax = min(a[1], b[1])
    # print(f"DEBUG a: {a}, b: {b}, maxmin {maxmin} minmax {minmax}")
    return maxmin <= minmax

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

    if have_overlap(interval[0], interval[1]):
        n_pairs_with_overlap += 1
    # print(f"DEBUG: ... ... n_pairs_with_overlap {n_pairs_with_overlap}")

print(f"RESULT: n_pairs_with_full_cont {n_pairs_with_full_cont}")
print(f"RESULT: n_pairs_with_overlap {n_pairs_with_overlap}")
