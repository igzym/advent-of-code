import sys

# To help prioritize item rearrangement, every item type can be converted to a priority:
# 
# Lowercase item types a through z have priorities 1 through 26.
# Uppercase item types A through Z have priorities 27 through 52.

input_file = sys.argv[1]

with open(input_file) as f:
    lines = f.readlines()

PRIO_SHIFT_LOWCASE = ord('a') - 1
PRIO_SHIFT_UPPCASE = ord('A') - 1 - 26
def tot_item_prio(itemset):
    tot_prio = 0
    for e in itemset:
        if e >= 'a' and e <= 'z':
            prio = ord(e) - PRIO_SHIFT_LOWCASE
        else:
            prio = ord(e) - PRIO_SHIFT_UPPCASE
        # print(f"DEBUG ... e {e} ({ord(e)}) prio {prio}")
        tot_prio += prio
        return tot_prio

tot_prio = 0
tot_prio_badge = 0

MAX_GROUP_SIZE = 3
cur_group_size = 0 # divide rucksacks in groups of size MAX_GROUP_SIZE
common_in_group = None
for ll in lines:
    rucksack = ll.strip()
    nitems = len(rucksack)
    assert nitems % 2 == 0, f"number of items {nitems} is not even"

    # print("DEBUG rucksack", rucksack)

    # part 1 common items in both compartments
    nitems_comp = nitems // 2
    comp1 = rucksack[:nitems_comp]
    comp2 = rucksack[nitems_comp:]
    common = set(comp1).intersection(comp2)

    # print("DEBUG comp1   ", comp1)
    # print("DEBUG comp2   ", comp2)
    # print("DEBUG common  ", common)

    tot_prio += tot_item_prio(common)

    # part 2 find the badge: only common item in all 3 rucksacks in group
    cur_group_size += 1
    if cur_group_size == 1:
        # first in group
        common_in_group = set(rucksack)
    else:
        common_in_group = common_in_group.intersection(set(rucksack))
    assert cur_group_size <= MAX_GROUP_SIZE
    if cur_group_size == MAX_GROUP_SIZE:
        # end of group
        assert len(common_in_group) == 1
        tot_prio_badge += tot_item_prio(common_in_group)
        # print(f"DEBUG common_in_group {common_in_group}")
        cur_group_size = 0
        common_in_group = None

print(f"RESULT: tot_prio       {tot_prio}")
print(f"RESULT: tot_prio_badge {tot_prio_badge}")
