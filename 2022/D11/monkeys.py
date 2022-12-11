import sys

import re

input_file = sys.argv[1]

with open(input_file) as f:
    lines = f.readlines()

monkey = dict()
cur_mid = None

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


for round in range(20):
    for mid in range(N):
        m = monkey[mid]
        for item in m['items']:
            m['n_inspected'] += 1
            old = item
            new = eval(m['op'])
            new = new // 3
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
print("expected for test input in part 1: 10605")
print("expected for actual input in part 1: 57838")