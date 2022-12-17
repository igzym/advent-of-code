# Day 15: Beacon Exclusion Zone

https://adventofcode.com/2022/day/15

- input: Sensor locations in a 2D grid with closest sensor reported
  by each one, using Manhattan distance; coordinates can be negative.
  For each sensor and beacon pair you know that no other beacon at
  distance closer or equal exist, so you can map areas of space
  that cannot contain a beacon 
- part 1: in row 2000000, how many positions cannot contain a beacon
- part 2: find the only position (x, y) that can contain a beacon given that
  the coordinate are restricted to the range [0, 4000000] in each dimension
  the expected answer is x*4000000 + y

To run the final version of the code:

For the example in the problem statement (small input)

    python beacon.py test_input.txt 10 0-20
  
For the actual full problem to generate the answer to the puzzles

    python beacon.py input.txt 2000000 0-4000000

Note that for the part 2 on full input it takes several minutes to run