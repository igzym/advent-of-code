D03 Gear Ratios
==================

https://adventofcode.com/2023/day/3

Run as

    python gear_ratios.py input.txt 1 # for part 1 answer
    python gear_ratios.py input.txt 1 # for part 2 answer

Rules
-----

- You are given a 2-D matrix representing a schematic of an engine
  containing some part numbers, recongized by being adjacent to a
  symbol
- Dot (.) is not a symbol

Part 1
------

- Find the sum of part numbers in the schematic

Part 2
------

- A `*` symbol is potentially a gear
- It is really a gear if it's adjacet to exactly two parts
- A gear ratio is the product of these two part numbers
- Find the sum of all gear ratios
