import sys

input_file = sys.argv[1]

# plays
# opponent
# A for Rock, B for Paper, and C for Scissors
# response

# Rock > Scissors > Paper > Rock

# scoring
# shape you played: 1 for Rock, 2 for Paper, and 3 for Scissors
# outcome: 0 if you lost, 3 if the round was a draw, and 6 if you won

# NOTE: implementation below using should be converted to lists with direct
# access by index if performance is of concern

# map strat codes to 'universal' shape codes: R(ock), P(aper), S(cissors)
shape_decode = {'A': 'R', 'B': 'P', 'C': 'S'}
resp_decode = {'X': 'R', 'Y': 'P', 'Z': 'S'}

# shape propertied and scoring
shape_score = {'R': 1, 'P': 2, 'S': 3}
outcome_score = {'L': 0, 'D': 3, 'W': 6}


# encode non-draw rules
outcome_rules = {
    'SP': 'W', 'SR': 'L',
    'RS': 'W', 'RP': 'L',
    'PR': 'W', 'PS': 'L',
}

def outcome(p, r):

    if r == p:
        return 'D' # draw

    return outcome_rules[r + p]

def score(p, r):
    outc = outcome(p, r)
    ssc = shape_score[r]
    osc = outcome_score[outc]
    sc = ssc + osc
    # print(f"DEBUG: {p} {r}: outc {outc} ssc {ssc} osc {osc} sc {sc}")
    return sc

with open(input_file) as f:
    lines = f.readlines()

total_score = 0

for ll in lines:
    pc, rc = ll.strip().split()
    p = shape_decode[pc]
    r = resp_decode[rc]

    sc = score(p, r)

    total_score += sc

print(f"RESULT: total_score {total_score}")
