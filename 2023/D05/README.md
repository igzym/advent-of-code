D05 If You Give A Seed A Fertilizer
====================================

https://adventofcode.com/2023/day/5

Run as

    python seeds.py input.txt 1 # for part 1 answer
    python seeds.py input.txt 1 # for part 2 answer

Rules
-----

To complicated to summarize in a few sentences, read the original at the link
above.

Technically, in your input you first get a list of seed types, represented as a
list of numeric ids, and series of maps which are sets by triples of form:

    DEST_START SOURCE_START LEN

For example

    37 93 3

means that the source range [93, 94, 45] maps to destination range [37, 38, 39]

Sources that don't match any map are mapped using an identity function.

There are 7 maps in the input, the location as the destination.

Part 1
------

Find the smallest location value for all the seeds at the input.

Part 2
------

tbd
