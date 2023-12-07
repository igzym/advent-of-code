D04 Scratchcards
==================

https://adventofcode.com/2023/day/4

Run as

    python scratchcards.py input.txt 1 # for part 1 answer
    python scratchcards.py input.txt 1 # for part 2 answer

Rules
-----

You get a set of cards like this one

    Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53

Left of `|` are the winning numbers, and on the right are the
numbers you have.

The worth of the card in points is $2^{n-1}$ where $n$ is the
number of numbers you have that match one of the winnng numbers.

In the above example $n=4$ (four winning numbers are 48, 83, 86, 17) so the
card value is 8 points.


Part 1
------

Sum of the points of all cards

Part 2
------

The number of points is actually used as the number of cards following the
current one that you make copies of; in subsequent processing you process
copies of the cards in the same way as the original cards.

### Example:

Your input is (see `example_input.txt`):

    Card 1: 41 48 | 41 48
    Card 2: 41 48 | 41  0
    Card 3: 41 48 |  0  0

This gives the following initial set of cards (value in parenthesis is the
card's value):

    Card 1 (2), Card 2 (1), Card 3 (0)

After you process the first card, whose value is two, you make a copy of the two
cards after it, cards 2 and 3:

    Card 1 (2), Card 2 (1), Card 3 (0)
                Card 2 (1), Card 3 (0)

Then you process each of the two copies of card 2, whose value is one, so you
make a copy of the one card that follows it:

    Card 1 (2), Card 2 (1), Card 3 (0)
                Card 2 (1), Card 3 (0)
                            Card 3 (0)
                            Card 3 (0)

Card 3 has a value of 0 so we stop creating copies. Note that even if the card
3 had some non-zero value we would stop because there are no cards that follow
it, and also if the card 2 had a value greater than one we would make copies of
only card 3 as there are no cards beyond that.

The answer is the total number of cards at the end, in this case it's 7
