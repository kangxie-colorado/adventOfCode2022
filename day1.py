def getMostCalories(filename):
    elf = -1
    maxCaloraies = 0
    with open(filename) as f:
        total = 0
        for line in f:
            if len(line.strip()) == 0:
                maxCaloraies = max(maxCaloraies, total)
                total = 0
            else:
                total += int(line.strip())

        # ugly code.. because the last part is not separated by a newline
        maxCaloraies = max(maxCaloraies, total)

    return maxCaloraies


def get3MostCalaries(filename):
    max3 = [0] * 3
    with open(filename) as f:
        total = 0
        for line in f:
            if len(line.strip()) == 0:
                # swap to max1/2/3 accordingly
                max3[0] = max(max3[0], total)
                if max3[0] > max3[1]:
                    # use a min heap might just avoid sort it
                    # but not much difference
                    max3.sort()
                total = 0
            else:
                total += int(line.strip())

        # ugly again.. why the last empty line don't get returned by f-handle?
        max3[0] = max(max3[0], total)

    return sum(max3)


if __name__ == '__main__':
    input_file = "day1_sample_input.txt"
    print(getMostCalories(input_file))
    print(get3MostCalaries(input_file))

    input_file = "day1_input.txt"
    print(getMostCalories(input_file))
    print(get3MostCalaries(input_file))
