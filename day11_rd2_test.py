from day11 import play, get_monkeys


def get_cases(filename):
    with open(filename) as f:
        rounds = []
        for line in f:
            if line.strip().startswith('=='):
                rd = int(line.strip().split()[-2])
                mks = [0]*4
            if line.strip().startswith("Monkey"):
                _, mk_id, _, _, count, _ = line.strip().split()
                mks[int(mk_id)] = int(count)
            if line.strip() == "":
                rounds.append((rd, mks))
            if line.strip() == 'EOF':
                break

    return rounds


if __name__ == '__main__':
    case_input_file = 'day11_rd2_test.txt'
    cases = get_cases(case_input_file)
    for case in cases:
        rd, expects = case
        mk_input_file = 'day11_sample.txt'
        mks = get_monkeys(mk_input_file)
        play(mks, rd, so_worried=True)

        got = [mk.inspected for mk in mks]
        assert got == expects