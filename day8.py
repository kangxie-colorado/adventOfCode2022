def get_forest(filename):
    forest = []
    with open(filename) as f:
        for line in f:
            row = []
            for c in line.strip():
                row.append(int(c))
            forest.append(row)
    return forest


def visible_trees(forest):
    m, n = len(forest), len(forest[0])
    visible = [[]] * m

    # row orientation scan
    for r in range(m):
        # the initialization can happen when going thru rows
        visible[r] = [0] * n
        visible[r][0] = visible[r][-1] = 1
        if r == 0 or r == m - 1:
            visible[r] = [1] * n

        leftHigh = forest[r][0]
        rightHigh = forest[r][-1]

        i, j = 1, n - 2
        # scan from left to right
        # same time also from right to left
        while i < n - 1:
            if forest[r][i] > leftHigh:
                visible[r][i] |= 1
                leftHigh = forest[r][i]
            if forest[r][j] > rightHigh:
                visible[r][j] |= 1
                rightHigh = forest[r][j]

            i, j = i + 1, j - 1

    # col orientation scan
    for c in range(1, n - 1):
        upHigh = forest[0][c]
        downHigh = forest[-1][c]

        i, j = 1, m - 2
        while i < m - 1:
            if forest[i][c] > upHigh:
                visible[i][c] |= 1
                upHigh = forest[i][c]
            if forest[j][c] > downHigh:
                visible[j][c] |= 1
                downHigh = forest[j][c]

            i, j = i + 1, j - 1

    return sum([sum(r) for r in visible])


# some thinking about how to do this as follows:
# scan from left to right, see which tree can see how far into left
# using a stack..
# 25512 -> stack: [(0,2)], the stack will be storing increasing numbers
# on 5, it can see upto the edge.. so 1 and stack becomes [(0,2), (1,5)..
# not a good example
# using 33549
# stack: [(0,3), (1,3)...]
# on 5.. it can see thru the edge..
# and it becomes the dominate tower for right further tree.. so only need to remember that
# okay.. maybe actually this is not a stack
# just need to keep knowing the so far highest tree to left and see if
# I can look pass it... but I need to keep the dist-so-far
# e.g. for this 5... it can looked to edge, which is 2..
# so if another 6 arrives, it can look thru the 5, and inherits its 2 without effort..
# .... hmm... stack still..
# and very annoying is, 3 look at 5, the dist is still 1 but not 0...
def scenic_scores(forest):
    m, n = len(forest), len(forest[0])
    scores = [[]] * m

    def scan(A, l):
        res = [1] * l
        stack = [(0, -1)]
        i = 1
        while i < l - 1:
            extendedStart = i
            while stack and A[stack[-1][0]] < A[i]:
                idx, start = stack.pop()
                extendedStart = start
                # at least 1, at most to the edge
                # edge nodes is init-ed to 0, so no matter to them
                res[idx] *= min(idx - start + 1, idx)

            stack.append((i, extendedStart))
            i += 1

        while stack:
            idx, start = stack.pop()
            res[idx] *= min(idx - start + 1, idx)

        return res

    # row orientation scan
    for r in range(m):
        # initialization also happens when going thru rows
        scores[r] = [1] * n
        scores[r][0] = scores[r][-1] = 0
        if r == 0 or r == m - 1:
            scores[r] = [0] * n
            continue

        left_to_right = scan(forest[r], n)
        right_to_left = scan(forest[r][::-1], n)[::-1]

        idx = 0
        for lScore,rScore in zip(left_to_right, right_to_left):
            scores[r][idx] *= lScore * rScore
            idx += 1

    for c in range(n):
        up_to_down = scan([r[c] for r in forest],m)
        bottom_to_top = scan([r[c] for r in forest][::-1], m)[::-1]
        idx = 0
        for uScore,dScore in zip(up_to_down, bottom_to_top):
            scores[idx][c] *= uScore * dScore
            idx += 1

    return max([max(i) for i in scores])


if __name__ == '__main__':
    input_file = 'day8_sample.txt'
    print(visible_trees(get_forest(input_file)))
    print(scenic_scores(get_forest(input_file)))

    input_file = 'day8_input.txt'
    print(visible_trees(get_forest(input_file)))
    print(scenic_scores(get_forest(input_file)))
