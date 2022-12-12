import math
from collections import deque


#
# def mul19(x):
#     return x * 19
#
#
# def add6(x):
#     return x + 6
#
#
# def square(x):
#     return x * x
#
#
# def add3(x):
#     return x + 3
#
#
# def noop(x):
#     return x


class MonkeyOp:
    def __init__(self, opStr="+", fixture=0):
        # default to x+0, which is a noop
        self.op = opStr
        self.fixture = fixture

    def __call__(self, x):
        if self.op == '+':
            return x + self.fixture
        if self.op == '*':
            return x * self.fixture
        if self.op == '**':
            return x * x

    def __repr__(self):
        if self.op != '**':
            return f"new = old {self.op} {self.fixture}"
        else:
            return f"new = old * old"


def noop(x):
    return MonkeyOp()(x)


class Monkey:
    def __init__(self, items=None, operation=None, test_divid=1, targets=None):
        self.items = items if items else deque()
        self.operation = operation if operation else noop
        self.test_divid = test_divid
        self.targets = targets if targets else []  # 0: True; 1: False
        self.inspected = 0

    def deal_item(self, monkeys, so_worried=False):
        # I guessed this... not sure why it works
        mod = math.prod([mk.test_divid for mk in monkeys])

        while self.items:
            item = self.items.popleft()
            # inspect/worry-rest
            item = self.operation(item)

            if so_worried:
                item %= mod
            else:
                item //= 3

            if item % self.test_divid == 0:
                monkeys[self.targets[0]].items.append(item)
            else:
                monkeys[self.targets[1]].items.append(item)
            self.inspected += 1


# 1. domain logic -- make sure it produces the right results
# 2. change operation to a class: with op and arg.. and implement __call__

# monkeys = [
#     Monkey(deque([79, 98]), MonkeyOp('*', 19), 23, [2, 3]),
#     Monkey(deque([54, 65, 75, 74]), MonkeyOp('+', 6), 19, [2, 0]),
#     Monkey(deque([79, 60, 97]), MonkeyOp('**'), 13, [1, 3]),
#     Monkey(deque([74, ]), MonkeyOp('+', 3), 17, [0, 1]),
# ]


def print_monkeys(mks, full=False):
    for mk in mks:
        if full:
            print(f"items: {mk.items}")
            print(f"    operation: {mk.operation}")
            print(f"    divisible?: {mk.test_divid}")
            print(f"    targets by true or false tests: {mk.targets}")
            print(f"I dealt {mk.inspected} items")
            print()
        else:
            print(mk.items, mk.inspected)


# for i in range(1, 21):
#     for mk in monkeys:
#         mk.deal_item()
#
#     print_monkeys(monkeys)


def get_monkeys(filename):
    res = []
    with open(filename) as f:
        for line in f:
            if line.strip() == 'EOF':
                break
            if line.strip().startswith('Monkey'):
                # a new monkey appears
                items = None
                mkOp = None
                divident = 1
                targets = []
            if line.strip() == "":
                # monkey is complete
                res.append(Monkey(items, mkOp, divident, targets))

            if line.strip().startswith("Starting items"):
                items = deque([int(item) for item in line.strip().split(':')[1].split(',')])
            if line.strip().startswith("Operation"):
                operator, fixture = line.strip().split('=')[1].split()[1:]
                if fixture == 'old':
                    operator = '**'
                    fixture = 0
                mkOp = MonkeyOp(operator, int(fixture))
            if line.strip().startswith("Test"):
                divident = int(line.strip().split()[-1])
            if line.strip().startswith('If true'):
                targets.append(int(line.strip().split()[-1]))
            if line.strip().startswith('If false'):
                targets.append(int(line.strip().split()[-1]))

    return res


def play(mks, rd, so_worried=False):
    for _ in range(rd):
        for mk in mks:
            mk.deal_item(mks, so_worried)


if __name__ == '__main__':
    # input_file = 'day11_sample.txt'
    # mks = get_monkeys(input_file)
    # play(mks, 10000, so_worried=True)
    # print_monkeys(mks, full=True)

    input_file = 'day11_input.txt'
    mks = get_monkeys(input_file)
    play(mks, 10000, so_worried=True)
    # print_monkeys(mks, full=True)
    print(sorted([mk.inspected for mk in mks]))