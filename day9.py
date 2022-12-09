def get_range_and_steps(filename):
    def apply_steps(pos, direction, steps):
        steps = int(steps)
        positions = []

        dir_coefficients = {
            'U': (1, 0),
            'D': (-1, 0),
            'L': (0, -1),
            'R': (0, 1),
        }
        xCo, yCo = dir_coefficients[direction]
        for step in range(1, steps + 1):
            positions.append([pos[0] + xCo * step, pos[1] + yCo * step])

        return positions

    with open(filename) as f:

        lastPos = [0, 0]
        up = down = left = right = 0
        steps = [lastPos]
        for line in f:
            positions = apply_steps(lastPos, *line.strip().split())
            lastPos = positions[-1]
            up = max(up, lastPos[0])
            down = min(down, lastPos[0])
            left = min(left, lastPos[1])
            right = max(right, lastPos[1])
            steps.extend(positions)

    return steps, [down, left], [up, right]


def calc_next_knot(prevX, prevY, knotX, knotY):
    # see if tail needs to move
    if abs(prevX - knotX) <= 1 and abs(prevY - knotY) <= 1:
        ...
    elif abs(prevX - knotX) + abs(prevY - knotY) >= 4:
        knotX = prevX - 1 if prevX > knotX else prevX + 1
        knotY = prevY - 1 if prevY > knotY else prevY + 1
    elif abs(prevX - knotX) + abs(prevY - knotY) == 3:
        # need to move diagonally
        if abs(prevX - knotX) == 1:
            # then head is moving horizontally
            knotX = prevX
            knotY = prevY - 1 if prevY > knotY else prevY + 1
        else:
            # headY - tailY abs to 1: head is moving vertically
            knotY = prevY
            knotX = prevX - 1 if prevX > knotX else prevX + 1
    elif (prevX == knotX or prevY == knotY) and abs(prevX - knotX) + abs(prevY - knotY) == 2:
        if abs(prevX - knotX) == 0:
            # then head moved horizontally
            knotY = prevY - 1 if prevY > knotY else prevY + 1
        else:
            # headY - tailY abs to 1: head is moving vertically
            knotX = prevX - 1 if prevX > knotX else prevX + 1

    return knotX, knotY


def simulation(steps, down_left, up_right):
    # re-coordinate to [0,0]
    d, l = down_left
    u, r = up_right
    u -= d
    r -= l
    m = u + 1
    n = r + 1
    mat = [[]] * m
    for i in range(m):
        mat[i] = [0] * n

    # DONE todo: a little problem, when d and l > 0
    # actually, not a problem.. because it starts from 0,0
    # so the bottom left is at most 0,0... d<=0, l<=0
    tailX = 0 - d
    tailY = 0 - l
    mat[tailX][tailY] = 1
    for headX, headY in steps:
        headX -= d
        headY -= l
        # mark the visited spot since I am already here
        tailX, tailY = calc_next_knot(headX, headY, tailX, tailY)
        mat[tailX][tailY] = 1

    return sum([sum(r) for r in mat])


def print_matrix(mat):
    mat = mat[::-1]
    for r in mat:
        s = ""
        for c in r:
            s = f"{s}#" if c == 1 else f"{s}."
        print(s)

    print()


"""
# off by 1!!!!!!!!???????
# holy shit!!!!! the input copy was wrong!!!!!
# copied again, the results are all good 
"""


def simulation2(steps, down_left, up_right):
    # re-coordinate to [0,0]
    d, l = down_left
    u, r = up_right
    u -= d
    r -= l
    m = u + 1
    n = r + 1
    mat = [[]] * m
    for i in range(m):
        mat[i] = [0] * n

    one_to_nine = [(0 - d, 0 - l)] * 9
    for prevX, prevY in steps:
        prevX -= d
        prevY -= l

        for i in range(9):
            nextX, nextY = one_to_nine[i]
            one_to_nine[i] = calc_next_knot(prevX, prevY, nextX, nextY)
            prevX, prevY = one_to_nine[i]

        knot9X, knot9Y = one_to_nine[8]
        mat[knot9X][knot9Y] |= 1

    print_matrix(mat)
    return sum([sum(r) for r in mat])

if __name__ == '__main__':
    input_file = 'day9_sample.txt'
    steps, down_left, up_right = get_range_and_steps(input_file)
    print(simulation(steps, down_left, up_right))
    print(simulation2(steps, down_left, up_right))

    input_file = 'day9_sample2.txt'
    steps, down_left, up_right = get_range_and_steps(input_file)
    print(simulation2(steps, down_left, up_right))
    """ the picture is like...
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    #.........................
    #.............###.........
    #............#...#........
    .#..........#.....#.......
    ..#..........#.....#......
    ...#........#.......#.....
    ....#......#.........#....
    .....#..............#.....
    ......#............#......
    .......#..........#.......
    ........#........#........
    .........########.........
    """

    input_file = 'day9_input.txt'
    steps, down_left, up_right = get_range_and_steps(input_file)
    print(simulation(steps, down_left, up_right))
    print(simulation2(steps, down_left, up_right))
