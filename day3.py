def find_same_char_in_both_half(s):
    h1 = s[:len(s) // 2]
    h2 = s[len(s) // 2:]

    return set(h1).intersection(set(h2))


def get_score(c):
    if 'a' <= c <= 'z':
        return ord(c) - ord('a') + 1
    if 'A' <= c <= 'Z':
        return ord(c) - ord('A') + 27
    return 0


def get_pri_sum(filename):
    res = 0
    with open(filename) as f:
        for line in f:
            dupChar = list(find_same_char_in_both_half(line.strip()))[0]
            res += get_score(dupChar)

    return res


def get_pri_sum_per_group(filename):
    with open(filename) as f:
        group = []
        res = 0
        for line in f:
            if len(group) < 3:
                group.append(line.strip())

            if len(group) == 3:
                badge = list(set(group[0]).intersection(set(group[1])).intersection(set(group[2])))[0]
                res += get_score(badge)
                group = []
        return res


if __name__ == '__main__':
    input_file = 'day3_sample.txt'
    print(get_pri_sum(input_file))
    print(get_pri_sum_per_group(input_file))

    input_file = 'day3_input.txt'
    print(get_pri_sum(input_file))
    print(get_pri_sum_per_group(input_file))
