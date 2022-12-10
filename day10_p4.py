

# Advent of Code 2022 Day 10
class CPU:
    def __init__(self, cycle=1, x_register=1):
        self.cycle = cycle
        self.x_register = x_register
        self.cycle_register_history = {}
        self.cycle_signal_history = {}

    def run_cycle(self, c_type, register=None):
        if c_type == "noop":
            self.cycle_register_history.update({self.cycle: self.x_register})
            self.cycle_signal_history.update({self.cycle: self.x_register * self.cycle})
            self.cycle += 1
        elif c_type == "addx":
            for i in range(2):
                self.cycle_register_history.update({self.cycle: self.x_register})
                self.cycle_signal_history.update({self.cycle: self.x_register * self.cycle})
                self.cycle += 1
            self.x_register += int(register)


# Import data
fname = "./day10_input.txt"
with open(fname) as f:
    commands = [(n.split()[0], n.strip().split()[1]) if "add" in n else (n.strip(), None) for n in f.readlines()]

elf_cpu = CPU()

for command in commands:
    elf_cpu.run_cycle(command[0], command[1])

# Part 1 Answer
print(f" Part 1 Answer: {sum([elf_cpu.cycle_signal_history.get(v) for v in list(range(20, 221, 40))])}")

# Part 2
cycles = [*elf_cpu.cycle_signal_history]
panels = [cycles[i: i + 240] for i in range(0, len(cycles), 240)]

display = ""
for panel in panels:
    for line in [panel[i: i + 40] for i in range(0, 240, 40)]:
        sprites = [n % 40 in list(map(lambda x: x + elf_cpu.cycle_register_history.get(n), range(0, 3, 1))) for n in line]
        display += "".join("#" if n else " " for n in sprites)
        display += "\n"
    display += "\n\n"

# Part 2 Answer
print(f" Part 2 Answer: \n{display}")