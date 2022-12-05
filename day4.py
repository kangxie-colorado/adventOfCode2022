def get_ranges(line):
    range1, range2 = line.split(',')
    start1, end1 = range1.split('-')
    start2, end2 = range2.split('-')
    return (int(start1), int(end1)), (int(start2), int(end2))


def fully_contain_pairs(filename):
    def full_contain(r1, r2):
        return (r1[0] <= r2[0] and r1[1] >= r2[1]) or (r2[0] <= r1[0] and r2[1] >= r1[1])

    res = 0
    with open(filename) as f:
        for line in f:
            range1, range2 = get_ranges(line.strip())
            if full_contain(range1, range2):
                res += 1
        return res


def overlapping_pairs(filename):
    def overlap(r1, r2):
        return not (r1[1] < r2[0] or r2[1] < r1[0])

    res = 0
    with open(filename) as f:
        for line in f:
            range1, range2 = get_ranges(line.strip())
            if overlap(range1, range2):
                res += 1
        return res


if __name__ == '__main__':
    filename = 'day4_sample.txt'
    print(fully_contain_pairs(filename))
    print(overlapping_pairs(filename))

    filename = 'day4_input.txt'
    print(fully_contain_pairs(filename))
    print(overlapping_pairs(filename))
