D06 Guard Gallivant
======================

https://adventofcode.com/2024/day/6

Run as

    python guard.py -part=1 input.txt

## Skill required

part 1 path tracing on a map
part 2 path tracing and identifying loop possibilities

The second part took way more time than expected. I was trying for some fancy solution of starting a simulated
walk from the current position when retracing the actual walk to find the cycles. But instead I should have
just restarted from the initial position and adding the potential obstacles one by one to face the states visited
in the actual walk (part1), and detecting if the walk in this new map ends off map or cycling.

Otherwise I was getting too many solutions.


## Answers

- part 1: 5312
- part 2: 1748
