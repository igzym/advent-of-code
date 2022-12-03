import sys

input_file = sys.argv[1]
#print(input_file)

with open(input_file) as f:
    lines = f.readlines()
    
#print('first 10 lines')
#print(lines[:10])

max_elf = 0
cur_elf = 0

for ll in lines:
    try:
        n = int(ll)
        cur_elf += n
    except ValueError:
        max_elf = max(max_elf, cur_elf)
        cur_elf = 0
    #print(f'cur_elf {cur_elf} max_elf {max_elf}')


# handle the last one
max_elf = max(max_elf, cur_elf)
#print(f'cur_elf {cur_elf} max_elf {max_elf}')

print(f"RESULT: max_elf calories: {max_elf}")
