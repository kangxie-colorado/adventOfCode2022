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
        visible[r] = [0] * n
        visible[r][0] = visible[r][-1] = 1
        if r == 0 or r == m - 1:
            visible[r] = [1] * n

        leftHigh = forest[r][0]
        rightHigh = forest[r][-1]

        i, j = 1, n - 2
        # scan from left to right
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


def scenic_scores(forest):
    m, n = len(forest), len(forest[0])
    scores = [[]] * m

    # row orientation scan
    for r in range(m):
        scores[r] = [1] * n
        scores[r][0] = scores[r][-1] = 0
        if r == 0 or r == m - 1:
            scores[r] = [0] * n
            continue

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

        # idx, start; idx-start will be the dist to see
        stack = [(0, -1)]
        i = 1
        while i < n - 1:
            extendedStart = i
            while stack and forest[r][stack[-1][0]] < forest[r][i]:
                idx, start = stack.pop()
                extendedStart = start
                # at least 1, at most to the edge
                scores[r][idx] *= min(idx - start + 1, idx)

            stack.append((i, extendedStart))
            i += 1

        while stack:
            idx, start = stack.pop()
            scores[r][idx] *= min(idx - start + 1, idx)

        # scan from right to left
        stack = [(n - 1, n - 1)]
        j = n - 2
        while j > 0:
            extendedStart = j
            while stack and forest[r][stack[-1][0]] < forest[r][j]:
                idx, start = stack.pop()
                extendedStart = start
                scores[r][idx] *= min(abs(idx - start) + 1, n - idx - 1)

            stack.append((j, extendedStart))
            j -= 1
        while stack:
            idx, start = stack.pop()
            scores[r][idx] *= min(abs(idx - start) + 1, n - idx - 1)

    for c in range(n):
        # top to down
        stack = [(0, -1)]
        i = 1
        while i < m - 1:
            extendedStart = i
            while stack and forest[stack[-1][0]][c] < forest[i][c]:
                idx, start = stack.pop()
                extendedStart = start
                # at least 1, at most to the edge
                scores[idx][c] *= min(idx - start + 1, idx)

            stack.append((i, extendedStart))
            i += 1

        while stack:
            idx, start = stack.pop()
            scores[idx][c] *= min(idx - start + 1, idx)

        # bottom to up
        stack = [(m - 1, m - 1)]
        j = m - 2
        while j > 0:
            extendedStart = j
            while stack and forest[stack[-1][0]][c] < forest[j][c]:
                idx, start = stack.pop()
                extendedStart = start
                scores[idx][c] *= min(abs(idx - start) + 1, n - idx - 1)

            stack.append((j, extendedStart))
            j -= 1
        while stack:
            idx, start = stack.pop()
            scores[idx][c] *= min(abs(idx - start) + 1, n - idx - 1)

    return max([max(i) for i in scores])



if __name__ == '__main__':
    input_file = 'day8_sample.txt'
    print(visible_trees(get_forest(input_file)))
    print(scenic_scores(get_forest(input_file)))

    input_file = 'day8_input.txt'
    print(visible_trees(get_forest(input_file)))
    print(scenic_scores(get_forest(input_file)))
