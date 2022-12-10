import sys

import re

input_file = sys.argv[1]

with open(input_file) as f:
    lines = f.readlines()

instructions = []  ## pairs of opcode, argument, where argument is None for noop

for ll in lines:
    vals = ll.strip("\n").split()
    opcode = vals[0]
    arg = int(vals[1]) if len(vals) > 1 else None
    instructions.append([opcode, arg])

cycles_per_op = {"noop": 1, "addx": 2}

reg_X = 1  # initial value of register X
cycle_n = 1  # cycle counter
signal_strength = 0  # the value we seek to calculate


for opcode, arg in instructions:
    clen = cycles_per_op[opcode]
    instr_clk = 1
    for clk in range(clen):
        if (cycle_n - 20) % 40 == 0:
            strength_incr = reg_X * cycle_n
            signal_strength += strength_incr
            # print(f"DEBUG cycle_n {cycle_n} strength {strength_incr}")
        # finalize operations at end of cycle
        if instr_clk == clen and opcode == "addx":
            reg_X = reg_X + arg
        cycle_n += 1
        instr_clk += 1

print(f"expected strength for test input 13140")
print(f"expected strength for final input 13760")
print(f"RESULT signal_strength {signal_strength}")
