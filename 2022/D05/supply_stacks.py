import sys

import re

input_file = sys.argv[1]

with open(input_file) as f:
    lines = f.readlines()

stack_lines = []
move_lines = []

def parse_stack(stack_line, n_stacks):
    stack_array = []
    for i in range(n_stacks):
        idx = i*4 + 1
        stack_array.append(stack_line[idx])
    return stack_array

def transpose_stacks(stacks):
    t_stacks = [[] for x in range(len(stacks[0]))]
    for stack in stacks:
        stack_row = 1
        for crate in stack:
            if crate != ' ':
                t_stacks[stack_row - 1].append(crate)
            stack_row += 1
    return t_stacks


def parse_move(move_line):
    ma = move_line.split()
    # returns tuple quantity, from, to
    return [int(x) for x in (ma[1], ma[3], ma[5])]


def get_top_crate_on_stack(t_stacks, stack_row):
    return t_stacks[stack_row-1][0]


def move_crates(t_stacks, quantity, from_stack, to_stack):
    moved = t_stacks[from_stack-1][:quantity]
    t_stacks[from_stack-1] = t_stacks[from_stack-1][quantity:]
    for c in moved:
        t_stacks[to_stack-1].insert(0, c)

def print_stacks(t_stacks):
    for stack in t_stacks:
        print([f"[{c}]" for c in stack])

def top_crates(t_stacks):
    r = ""
    for stack in t_stacks:
        r += stack[0]
    return r

stack_input = True # stacks are in the beginning sep from moves by empty line

for ll in lines:
    ll = ll.strip("\n")
    if ll == '':
        # end of stacks config, moves will follow
        stack_ids_line = stack_lines.pop()
        n_stacks = [int(x) for x in  stack_ids_line.split()][-1]
        stack_input = False
        continue

    if stack_input:
        stack_lines.append(ll)
    else:
        move_lines.append(ll)

stacks = []
moves = []
for stack_line in stack_lines:
    stacks.append(parse_stack(stack_line, n_stacks))
for move_line in move_lines:
    moves.append(parse_move(move_line))

t_stacks = transpose_stacks(stacks)

for stack in t_stacks:
    pass #print(f"DEBUG: stack {stack}")
for move in moves:
    pass #print(f"DEBUG: move {move}")

#print_stacks(t_stacks)
for move in moves:
    quantity, from_stack, to_stack = move[0], move[1], move[2]
    #print('move', quantity, from_stack, to_stack)
    move_crates(t_stacks, quantity, from_stack, to_stack)
    #print_stacks(t_stacks)

print(f"RESULT top crates: {top_crates(t_stacks)}")
