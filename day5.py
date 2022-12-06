def get_stack_lines(filename):
    lines = 0
    with open(filename) as f:
        stack_lines = []
        for line in f:
            lines += 1
            if len(line.strip()) == 0:
                return lines, stack_lines[::-1]

            stack_lines.append(line.rstrip())
        return 0, None


def init_stack(stack_lines):
    # padding for ease of index use in the instructions
    no_of_stacks = len(stack_lines[0].split()) + 1
    stacks = [None] * no_of_stacks
    for i in range(no_of_stacks):
        stacks[i] = []

    for line in stack_lines[1:]:
        for i in range(0, len(line), 4):
            if line[i:i + 3] != "   ":
                stacks[i // 4 + 1].append(line[i:i + 3][1])

    return stacks


def move_crates(filename, skip, stacks):
    with open(filename) as f:
        for line in f:
            if skip:
                skip -= 1
                continue

            _, num, _, s, _, d = line.strip().split()
            num, s, d = int(num), int(s), int(d)
            # move one at a time
            while num:
                stacks[d].append(stacks[s].pop())
                num -= 1

    return "".join([s[-1] for s in stacks[1:]])


def move_crates2(filename, skip, stacks):
    with open(filename) as f:
        for line in f:
            if skip:
                skip -= 1
                continue

            _, num, _, s, _, d = line.strip().split()
            num, s, d = int(num), int(s), int(d)
            # move num at a time
            stacks[d].extend(stacks[s][-num:])
            stacks[s] = stacks[s][:-num]

    return "".join([s[-1] for s in stacks[1:]])


if __name__ == '__main__':
    input_file = 'day5_sample.txt'
    line_to_instructions, stack_lines = get_stack_lines(input_file)
    print(move_crates(input_file, line_to_instructions, init_stack(stack_lines)))
    print(move_crates2(input_file, line_to_instructions, init_stack(stack_lines)))

    input_file = 'day5_input.txt'
    line_to_instructions, stack_lines = get_stack_lines(input_file)
    print(move_crates(input_file, line_to_instructions, init_stack(stack_lines)))
    print(move_crates2(input_file, line_to_instructions, init_stack(stack_lines)))
