# A for Rock, B for Paper, and C for Scissors.
# X for Rock, Y for Paper, and Z for Scissors

scores = {
    'X': 1,
    'Y': 2,
    'Z': 3,
    'A': 1,
    'B': 2,
    'C': 3,
}

winDrawLoss = {
    'XC': 6,
    'XA': 3,
    'XB': 0,
    'YA': 6,
    'YB': 3,
    'YC': 0,
    'ZB': 6,
    'ZC': 3,
    'ZA': 0,
}

scoresRD2 = {
    'X': 0,
    'Y': 3,
    'Z': 6,
}

winDrawLossRD2 = {
    'XA': scores['C'],
    'XB': scores['A'],
    'XC': scores['B'],

    'YA': scores['A'],
    'YB': scores['B'],
    'YC': scores['C'],

    'ZA': scores['B'],
    'ZB': scores['C'],
    'ZC': scores['A'],
}


def getScore(fn):
    with open(fn) as f:
        score = 0
        for line in f:
            elf, me = line.split()
            score += scores[me] + winDrawLoss[f"{me}{elf}"]

    return score


def getScoreRD2(fn):
    with open(fn) as f:
        score = 0
        for line in f:
            elf, me = line.split()
            score += scoresRD2[me] + winDrawLossRD2[f"{me}{elf}"]

    return score


if __name__ == '__main__':
    filename = 'day2_sample.txt'
    print(getScore(filename))
    print(getScoreRD2(filename))

    filename = 'day2_input.txt'
    print(getScore(filename))
    print(getScoreRD2(filename))