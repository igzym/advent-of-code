# Day 12: Hill Climbing Algorithm

https://adventofcode.com/2022/day/12

- Input: heightmap of the surrounding area as a grid of characters, a, b, ...Z encoding increasing height
  and the starting (S, elevation z) and ending point (E, elevation z)
- Part 1 puzzle: find shortest path from S to E, with constraint that when going up in height
  you can go at most one step in height (eg, from a to b), but you can go down in elevation any distance
- Idea: translate the grid into a graph and run one of the well known shortest path algorithms
- Part 2 puzzle: find shortest path from any square 'a'
