import sys

# To help prioritize item rearrangement, every item type can be converted to a priority:
# 
# Lowercase item types a through z have priorities 1 through 26.
# Uppercase item types A through Z have priorities 27 through 52.

input_file = sys.argv[1]

with open(input_file) as f:
    lines = f.readlines()

tot_prio = 0

PRIO_SHIFT_LOWCASE = ord('a') - 1
PRIO_SHIFT_UPPCASE = ord('A') - 1 - 26

for ll in lines:
    rucksack = ll.strip()
    nitems = len(rucksack)
    assert nitems % 2 == 0, f"number of items {nitems} is not even"

    # print("DEBUG rucksack", rucksack)

    nitems_comp = nitems // 2
    comp1 = rucksack[:nitems_comp]
    comp2 = rucksack[nitems_comp:]
    common = set(comp1).intersection(comp2)

    # print("DEBUG comp1   ", comp1)
    # print("DEBUG comp2   ", comp2)
    # print("DEBUG common  ", common)

    prio = 0
    for e in common:
        if e >= 'a' and e <= 'z':
            prio = ord(e) - PRIO_SHIFT_LOWCASE
        else:
            prio = ord(e) - PRIO_SHIFT_UPPCASE
        # print(f"DEBUG ... e {e} ({ord(e)}) prio {prio}")

    tot_prio += prio


print(f"RESULT: tot_prio {tot_prio}")
