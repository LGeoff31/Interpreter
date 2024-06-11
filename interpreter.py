import sys

# read arguments
program_filepath = sys.argv[1]

# read file lines
program_lines = []
with open(program_filepath, "r") as program_file:
    program_lines = [line.strip() for line in program_file.readlines()]
program = []
token_counter = 0  # where we are in our program
label_tracker = {}  # which index list our label is pointing to

for line in program_lines:
    parts = line.split(" ")
    opcode = parts[0]
    # prevent error user enters empty line
    if opcode == "":
        continue

    if opcode.endswith(":"):  # check label or loop
        label_tracker[opcode[:-1]] = token_counter
        continue

    program.append(opcode)
    token_counter += 1

    # operations
    if opcode == "PUSH":
        number = int(parts[1])
        program.append(number)
        token_counter += 1
    elif opcode == "PRINT":
        string_literal = ' '.join(parts[1:])[1:-1]
        program.append(string_literal)
        token_counter += 1
    elif opcode == "JUMP.EQ.0":
        label = parts[1]
        program.append(label)
        token_counter += 1
    elif opcode == "JUMP.GT.0":
        label = parts[1]
        program.append(label)
        token_counter += 1

# interpret program


class Stack:
    def __init__(self, size):
        self.buf = [0 for _ in range(size)]
        self.sp = -1

    def push(self, number):
        self.sp += 1
        self.buf[self.sp] = number

    def pop(self):
        number = self.buf[self.sp]
        self.sp -= 1
        return number

    def top(self):
        return self.buf[self.sp]


pc = 0
stack = Stack(256)  # 2^8

while program[pc] != "HALT":
    opcode = program[pc]
    pc += 1

    if opcode == "PUSH":
        stack.push(program[pc])
        pc += 1
    elif opcode == "POP":
        stack.pop()
    elif opcode == "ADD":
        a, b = stack.pop(), stack.pop()
        stack.push(a+b)
    elif opcode == "SUB":
        a, b = stack.pop(), stack.pop()
        stack.push(b-a)
    elif opcode == "PRINT":
        string_literal = program[pc]
        pc += 1
        print(string_literal)
    elif opcode == "READ":
        number = int(input())
        stack.push(number)
    elif opcode == "JUMP.EQ.0":
        number = stack.top()
        if number == 0:
            pc = label_tracker[program[pc]]
        else:
            pc += 1
    elif opcode == "JUMP.GT.0":
        number = stack.top()
        if number > 0:
            pc = label_tracker[program[pc]]
        else:
            pc += 1
