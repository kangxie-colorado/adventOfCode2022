# wow! just used a little TDD to help design the algorithm
# it turns out to be correct
import ast
from functools import cmp_to_key


def parse_array_from_string(s):
    # keep the current run(a ref) at the top of stack
    # when this run finishes, append it to its parent run
    # which is at the stack top
    # it is already the root run.. then all is done
    stack = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == "[":
            curr = []
            stack.append(curr)
        elif c == "]":
            run = stack.pop()
            if stack:
                curr = stack[-1]
                curr.append(run)
        elif c == ",":
            ...
        elif c.isdigit():
            num = c
            j = i + 1
            while s[j].isdigit():
                num += s[j]
                j += 1
            curr.append(int(num))
            i = j - 1
        i += 1
    return curr


def parse_array_from_string(s):
    # credit to Sean: just use ast.literal_eval
    return ast.literal_eval(s)


def compare_arrays(A, B):
    if not A and B:
        return True
    if not B and A:
        return False
    if not A and not B:
        return False

    for a, b in zip(A, B):
        if type(a) is list and type(b) is list:
            return compare_arrays(a, b) or (a == b and compare_arrays(A[1:], B[1:]))
        elif type(a) is list or type(b) is list:
            # a number compares to a list
            if type(a) is int:
                return compare_arrays([a, ], b, ) or ([a, ] == b and compare_arrays(A[1:], B[1:]))
            else:
                return compare_arrays(a, [b, ], ) or (a == [b, ] and compare_arrays(A[1:], B[1:]))
        else:
            return a < b or (a == b and compare_arrays(A[1:], B[1:]))

    return False


def compare_arrays_sort(A, B):
    if not A and B:
        return -1
    if not B and A:
        return 1
    if not A and not B:
        return 0

    for a, b in zip(A, B):
        if type(a) is list and type(b) is list:
            return compare_arrays_sort(a, b) or compare_arrays_sort(A[1:], B[1:])
        elif type(a) is list or type(b) is list:
            # a number compares to a list
            if type(a) is int:
                return compare_arrays_sort([a, ], b, ) or compare_arrays_sort(A[1:], B[1:])
            else:
                return compare_arrays_sort(a, [b, ], ) or compare_arrays_sort(A[1:], B[1:])
        else:
            if a < b:
                return -1
            elif a > b:
                return 1
            else:
                return compare_arrays_sort(A[1:], B[1:])

    return 0


def correct_pairs(filename):
    correct = []
    pairIdx = 1
    i = 0
    with open(filename) as f:
        pair = [[], []]
        for line in f:
            line = line.strip()
            if line == "EOF":
                break

            if line == "":
                if compare_arrays_sort(pair[0], pair[1]) == -1:
                    correct.append(pairIdx)
                pair = [[], []]
                pairIdx += 1
                continue
            pair[i] = parse_array_from_string(line)
            i ^= 1

    return sum(correct)


def decoder_key(filename):
    packets = [[[2]], [[6]]]
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line == "" or line == "EOF":
                continue
            packets.append(parse_array_from_string(line))

    packets.sort(key=cmp_to_key(compare_arrays_sort))
    prod = 1
    for i, p in enumerate(packets):
        if p in ([[2]], [[6]]):
            prod *= i + 1

    return prod


if __name__ == "__main__":
    input_file = "day13_sample.txt"
    print(correct_pairs(input_file))
    print(decoder_key(input_file))

    input_file = "day13_input.txt"
    print(correct_pairs(input_file))
    print(decoder_key(input_file))
