D02 Cube Conundrum
==================

https://adventofcode.com/2023/day/2

Run as

    python cube_conundrum.py input.txt 1 # for part 1 answer
    python cube_conundrum.py input.txt 1 # for part 2 answer

Rules
-----

- In each game Elf hides a certain set of bag of cubes of 3 colours, red, green
  or blue
- Elf makes several random draws from the bag and shows them to you
- Several games like this are played

Part 1
------

- You have to determine which games would have been possible if there were only
  only 12 red cubes, 13 green cubes, and 14 blue cubes in the bag
- For example, if the elf showed you a draw with 13 red cubes, that game would
  not be possible
- Add IDs of these games to get the answer

Part 2
------

- for each game calculate the minimum number of cubes of each colour that must
  have been present for the game to be possible
- the power of a game is a product of these counts
- the answer is the sum of the power of all games
