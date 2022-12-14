# I'll just use a 1000*1000 matrix
# swap x,y from input.. to be aligned with natrual orientation

def print_matrix(mat, x_start, x_end, y_start, y_end):
    print(f"Columns: {y_start} to {y_end}")
    m, n = len(mat), len(mat[0])
    for i in range(m):
        row = f'{i:< 3}    '
        for j in range(n):
            if y_start <= j <= y_end:
                row = f"{row}{mat[i][j]}"
        if x_start <= i <= x_end:
            print(row)

    print()


def init_matrix(filename):
    mat = [['.'] * 2000 for _ in range(1000)]
    mat[0][500] = '+'
    bottom = 0

    with open(filename) as f:
        for line in f:
            steps = line.strip().split()[::2]
            # swapping x and y
            for start, end in zip(steps, steps[1:]):
                y1, x1 = start.split(',')
                y2, x2 = end.split(',')
                x1, x2, y1, y2 = int(x1), int(x2), int(y1), int(y2)

                if x1 == x2:
                    x = x1
                    for y in range(min(y1, y2), max(y1, y2) + 1):
                        mat[x][y] = '#'
                if y1 == y2:
                    y = y1
                    for x in range(min(x1, x2), max(x1, x2) + 1):
                        mat[x][y] = '#'

                if mat[x][y] == '#':
                    bottom = max(bottom, x)

    return mat, bottom


def simulation(mat, bottom):
    currX, currY = 0, 500
    unit = 0

    while currX <= bottom:
        # always go the first rest position
        # assume no boundary will be reach at this point
        # todo: test currY-1 against the boundary
        #  -- may not need to because I can always shift the matrix to make it work
        if mat[currX + 1][currY] == '.' or mat[currX + 1][currY - 1] == '.' or mat[currX + 1][currY + 1] == '.':
            if mat[currX + 1][currY] == '.':
                ...
            elif mat[currX + 1][currY - 1] == '.':
                currY -= 1
            else:
                currY += 1
            currX += 1
        else:
            # rest
            unit += 1
            mat[currX][currY] = 'o'
            currX, currY = 0, 500

    # print last sand trails
    currX, currY = 0, 500
    while currX <= bottom + 3:
        if mat[currX + 1][currY] == '.' or mat[currX + 1][currY - 1] == '.' or mat[currX + 1][currY + 1] == '.':
            if mat[currX + 1][currY] == '.':
                ...
            elif mat[currX + 1][currY - 1] == '.':
                currY -= 1
            else:
                currY += 1
            currX += 1
            mat[currX][currY] = '~'

    return unit


def simulation2(mat, bottom):
    for j in range(len(mat[0])):
        mat[bottom][j] = '#'

    currX, currY = 0, 500
    unit = 0
    while currX <= bottom:
        # always go the first rest position
        # assume no boundary will be reach at this point
        # todo: test currY-1 against the boundary
        #  -- may not need to because I can always shift the matrix to make it work
        if mat[currX + 1][currY] == '.' or mat[currX + 1][currY - 1] == '.' or mat[currX + 1][currY + 1] == '.':
            if mat[currX + 1][currY] == '.':
                ...
            elif mat[currX + 1][currY - 1] == '.':
                currY -= 1
            else:
                currY += 1
            currX += 1
        else:
            # rest
            unit += 1
            mat[currX][currY] = 'o'
            if currX == 0 and currY == 500:
                break
            currX, currY = 0, 500

    return unit


if __name__ == '__main__':
    input_file = 'day14_sample.txt'
    mat, bottom = init_matrix(input_file)
    print_matrix(mat, 0, 12, 480, 530)
    # print(simulation(mat, bottom))
    print(simulation2(mat, bottom + 2))
    print_matrix(mat, 0, 12, 480, 530)

    input_file = 'day14_input.txt'
    mat, bottom = init_matrix(input_file)
    print_matrix(mat, 0, 200, 50, 600)

    # print(simulation(mat, bottom))
    print(simulation2(mat, bottom + 2))
    print_matrix(mat, 0, 160, 100, 800)
