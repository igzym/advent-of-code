import sys

input_file = sys.argv[1]

with open(input_file) as f:
    lines = f.readlines()
    
# keep track of all elves calories
elf_cal = []

cur_elf = 0

for ll in lines:
    try:
        n = int(ll)
        cur_elf += n
    except ValueError:
        elf_cal.append(cur_elf)
        cur_elf = 0
    #print(f'cur_elf {cur_elf}')


# handle the last one
if cur_elf > 0:
    elf_cal.append(cur_elf)
    cur_elf = 0

n_elf = len(elf_cal)

top_elf = sorted(range(n_elf), key=lambda i: elf_cal[i], reverse=True)

max_elf = elf_cal[top_elf[0]]

print(f"RESULT: max_elf calories: {max_elf}")


top_N = 3

N_to_display = 5

print('top elf ids')
print(top_elf[:N_to_display])
print('top elf weights')
print([elf_cal[i] for i in top_elf[:N_to_display]])

top_N_cal = sum([elf_cal[i] for i in top_elf[:top_N]])

print(f"RESULT: total calories in top {top_N} elves: {top_N_cal}")

