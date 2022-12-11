import sys

import re

sys.argv.pop(0)  # get rid of first argument - script name
input_file = sys.argv.pop(0)

n_rounds = 10000  # part 2 value, was 20 in round 1
if sys.argv:
    n_rounds = int(sys.argv.pop(0))  # optional number of arguments as command line parameter
print("n_rounds", n_rounds)

# are we in part 1 (divide worry level by 3 to keep it manageable) or part 2 ?
part_2 = True
if sys.argv:
    part_str = sys.argv.pop(0)
    assert part_str in ["part_1", "part_2"]
    part_2 = part_str == "part_2"
print("part_2", part_2)


with open(input_file) as f:
    lines = f.readlines()

monkey = dict()
cur_mid = None

# calculate the common divisor as a product of all individual divisors of
# different monkeys
# it will be used to reduce the worry level to keep it growing exponentially
# without changing its various divisibility tests
common_divisor = 1

for ll in lines:
    ll = ll.strip()  # get rid of trailing newline AND any leading whitespace
    m = re.match(r'Monkey (\d+)', ll)
    if m:
        cur_mid = int(m.group(1))
        monkey[cur_mid] = dict()
        monkey[cur_mid]['id'] = cur_mid
        monkey[cur_mid]['n_inspected'] = 0  # total number of items inspected
        continue

    m = re.match(r'Starting items: (.*)', ll)
    if m:
        items_str = m.group(1)
        monkey[cur_mid]['items'] = [int(x) for x in items_str.split(', ')]
        continue

    m = re.match(r'Operation: (.*)', ll)
    if m:
        op_str = m.group(1)
        m = re.match('new = (.*)', op_str)
        assert m, f"unexpected operation format '{op_str}'"
        monkey[cur_mid]['op'] = m.group(1)
        continue

    m = re.match(r'Test: divisible by (.*)', ll)
    if m:
        test_div = int(m.group(1))
        monkey[cur_mid]['test_div'] = test_div
        common_divisor *= test_div
        continue

    m = re.match(r'If true: throw to monkey (.*)', ll)
    if m:
        to_monkey = int(m.group(1))
        monkey[cur_mid]['to_monkey_true'] = to_monkey
        continue

    m = re.match(r'If false: throw to monkey (.*)', ll)
    if m:
        to_monkey = int(m.group(1))
        monkey[cur_mid]['to_monkey_false'] = to_monkey
        continue

N = len(monkey)  # number of monkeys


def print_monkey(m):
    items = ", ".join([str(x) for x in m['items']])
    print(f"Monkey {m['id']}: {items}   (inspected: {m['n_inspected']})")


for round in range(n_rounds):
    for mid in range(N):
        m = monkey[mid]
        for item in m['items']:
            m['n_inspected'] += 1
            old = item
            new = eval(m['op'])
            if not part_2:
                # part 1 - keep it manageable by dividing it
                # by constant value 3
                new = new // 3
            else:
                # part 2 - need to reduce the value to keep it manageable
                # differently
                new = new % common_divisor
            if new % m['test_div'] == 0:
                to_monkey = monkey[m['to_monkey_true']]
            else:
                to_monkey = monkey[m['to_monkey_false']]
            to_monkey['items'].append(new)
        # all items inspected, reset 'bag' to empty
        # it may get filled up again before the end of the round
        # if other monkeys sends us items
        m['items'] = []

    # print(f"after round {round+1}")
    # for mid in range(N):
    #     print(f"Monkey {mid}")
    #     print(f"... {monkey[mid]}")

 
# print(f"after {round+1}")
for mid in range(N):
    print_monkey(monkey[mid])


# sort by descending number of items inspectedd to
# determine the two most active monkeys

by_act = [(mid, monkey[mid]['n_inspected']) for mid in range(N)]
by_act = sorted(by_act, key = lambda item: item[1], reverse = True)

# multiply the number of inspected items of the two most
# active monkeys
m1 = by_act[0]
m2 = by_act[1]
monkey_business = m1[1] * m2[1]

print(f"RESULT monkey_business {monkey_business} (by {m1} and {m2}")
print("-- part 1 --")
print("expected for test input: 10605")
print("expected for actual input: 57838")
print("-- part 2 --")
print("expected for test input: 2713310158")
print("expected for actual input: 15050382231")
