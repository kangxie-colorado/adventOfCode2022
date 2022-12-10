def get_six_signal(filename):
    def calc_score(c, v):
        res = 0
        if c in {20, 60, 100, 140, 180, 220}:
            res = v * c
        return res

    cycle = 0
    val = 1
    signal_strength = 0
    with open(filename) as f:
        for line in f:
            instr = line.strip().split()[0]
            if instr == 'noop':
                cycle += 1
                cycle_score = calc_score(cycle, val)
            else:
                # val stay the same before instruction ends
                # interval vs point in time... messed me up
                # really I should think more before coding
                cycle += 2
                cycle_score = calc_score(cycle - 1, val) or calc_score(cycle, val)

                delta = int(line.strip().split()[1])
                val += delta

            # interval vs cycle
            signal_strength += cycle_score
    return signal_strength


def print_crt(crt):
    for r in crt:
        print(''.join(r))

    print()


def crt_screen(filename):
    screen = [[]] * 6
    for i in range(6):
        screen[i] = [' '] * 40

    # X 1 covers pos 0-1
    X = 1
    row = 0
    crt_pos = 0
    with open(filename) as f:
        for line in f:
            instr = line.strip().split()[0]
            drawing = 1 if instr == 'noop' else 2

            while drawing:
                if crt_pos in range(X - 1, X + 2):
                    screen[row][crt_pos] = '#'

                crt_pos += 1
                if crt_pos == 40:
                    crt_pos = 0
                    row += 1
                drawing -= 1

            if instr == 'addx':
                delta = int(line.strip().split()[1])
                X += delta

        print_crt(screen)


if __name__ == '__main__':
    input_file = 'day10_sample.txt'
    print(get_six_signal(input_file))
    crt_screen(input_file)

    input_file = 'day10_input.txt'
    print(get_six_signal(input_file))
    crt_screen(input_file)
