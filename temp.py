class MonkeyOp:
    def __init__(self, opStr, fixture=None):
        self.op = opStr
        self.fixture = fixture

    def __call__(self, x):
        if self.op == '+':
            return x + self.fixture
        if self.op == '*':
            return x * self.fixture
        if self.op == '**':
            return x * x


op1 = MonkeyOp('+', 3)
op2 = MonkeyOp('*', 19)
print(op1(5))
print(op2(4))

op3 = MonkeyOp('**', 0)
print(op3(6))

with open('day15.txt', 'w') as f:
    print(123, file=f)
