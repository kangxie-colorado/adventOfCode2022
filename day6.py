from collections import Counter


def first_marker_right(s, marker):
    j = marker
    wind = Counter(s[0:marker])
    while j < len(s):
        if len(wind) == marker:
            return j

        wind[s[j]] += 1

        i = j - marker
        wind[s[i]] -= 1
        if wind[s[i]] == 0:
            wind.pop(s[i])

        j += 1
    return -1


if __name__ == '__main__':
    assert first_marker_right('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 4) == 7
    assert first_marker_right('nppdvjthqldpwncqszvftbrmjlhg', 4) == 6
    assert first_marker_right('bvwbjplbgvbhsrlpgdmjqwftvncz', 4) == 5
    assert first_marker_right('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 4) == 10
    assert first_marker_right('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 4) == 11

    input_file = "day6_input.txt"
    print(first_marker_right(open(input_file).read().strip(), 4))

    assert first_marker_right('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 14) == 19
    assert first_marker_right('nppdvjthqldpwncqszvftbrmjlhg', 14) == 23
    assert first_marker_right('bvwbjplbgvbhsrlpgdmjqwftvncz', 14) == 23
    assert first_marker_right('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 14) == 29
    assert first_marker_right('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 14) == 26
    print(first_marker_right(open(input_file).read().strip(), 14))