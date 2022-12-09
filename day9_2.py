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
        for step in range(steps + 1):
            positions.append([pos[0] + xCo * step, pos[1] + yCo * step])

        return positions

    with open(filename) as f:
        lastPos = [0, 0]
        steps = [lastPos]
        for line in f:
            positions = apply_steps(lastPos, *line.strip().split())
            lastPos = positions[-1]
            steps.extend(positions)

    return steps


def next_knot(prev, knot):
    prevX, prevY = prev
    knotX, knotY = knot

    if abs(prevX - knotX) <= 1 and abs(prevY - knotY) <= 1:
        ...
    elif abs(prevX - knotX) >= 2 and abs(prevY - knotY) >= 2:
        knotX = prevX - 1 if prevX > knotX else prevX + 1
        knotY = prevY - 1 if prevY > knotY else prevY + 1
    elif (abs(prevX - knotX) == 1 or abs(prevY - knotY) == 1) and abs(prevX - knotX) + abs(prevY - knotY) >= 3:
        # need to move diagonally
        if abs(prevX - knotX) == 1:
            # then head is moving horizontally
            knotX = prevX
            knotY = prevY - 1 if prevY > knotY else prevY + 1
        else:
            # headY - tailY abs to 1: head is moving vertically
            knotY = prevY
            knotX = prevX - 1 if prevX > knotX else prevX + 1
    elif (abs(prevX - knotX) == 0 or abs(prevY - knotY) == 0) and abs(prevX - knotX) + abs(prevY - knotY) >= 2:
        if abs(prevX - knotX) == 0:
            # then head moved horizontally
            knotY = prevY - 1 if prevY > knotY else prevY + 1
        else:
            # headY - tailY abs to 1: head is moving vertically
            knotX = prevX - 1 if prevX > knotX else prevX + 1

    return knotX, knotY


def simulation(steps):
    p1 = set()
    p2 = set()

    knots = [(0, 0)] * 9
    for head in steps:
        p1.add(knots[0])
        p2.add(knots[8])
        knots[0] = next_knot(head, knots[0])
        for i in range(1, 9):
            knots[i] = next_knot(knots[i - 1], knots[i])
        p1.add(knots[0])
        p2.add(knots[8])

    return len(p1), len(p2)


if __name__ == '__main__':
    input_file = 'day9_sample.txt'
    steps = get_range_and_steps(input_file)
    print(simulation(steps))

    input_file = 'day9_sample2.txt'
    steps = get_range_and_steps(input_file)
    print(simulation(steps))

    input_file = 'day9_input.txt'
    steps = get_range_and_steps(input_file)
    print(simulation(steps))
