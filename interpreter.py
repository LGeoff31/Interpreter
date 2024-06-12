"""

Supported Operations:

READ: Reads a user input as and stores it on the stack as an integer
LOG X:  Outputs to terminal string X

ADD: Returns the sum of the two most recent READ integers
SUBTRACT: Returns the difference of the first READ integer SUBTRACTtracted from the second

IF_0_GOTO L1: If the top of the stack is 0, jump to the function L1
IF_GT_0_GOTO LOOP: If top stack greater than 0, jump up to start LOOP

POP: Removes the top of the stack and returns it
END: Ends the program

"""

"""
New Features to implement:

- String input parsing
- Multiplication / Division / Modulus
- Conditionals

"""

# Retrieve filepath from command-line argument of program want to execute
import sys
program_filepath = sys.argv[1]

# Extract all lines of input from textfile removing leading and trailing whitespace
with open(program_filepath, "r") as program_file:
    program_lines = [line.strip() for line in program_file.readlines()]

program = []
token_counter = 0
label_tracker = {}

# Process all the tokens into program, allowing for easy processing
for line in program_lines:
    parts = line.split(" ")
    opcode = parts[0]

    if opcode == "":
        continue

    # Store LOOP or function index to travel there when needed
    if opcode.endswith(":"):
        label_tracker[opcode[:-1]] = token_counter
        continue

    program.append(opcode)
    token_counter += 1

    if opcode == "PUSH":
        number = int(parts[1])
        program.append(number)
        token_counter += 1
    elif opcode == "LOG":
        string_literal = ' '.join(parts[1:])[1:-1]
        program.append(string_literal)
        token_counter += 1
    elif opcode == "IF_0_GOTO":
        label = parts[1]
        program.append(label)
        token_counter += 1
    elif opcode == "IF_GT_0_GOTO":
        label = parts[1]
        program.append(label)
        token_counter += 1


# Process the file commands in program
class Stack:
    def __init__(self, size):
        self.lst = [0 for _ in range(size)]
        self.idx = -1

    def push(self, number):
        self.idx += 1
        self.lst[self.idx] = number

    def pop(self):
        number = self.lst[self.idx]
        self.idx -= 1
        return number

    def top(self):
        return self.lst[self.idx]


i = 0
stack = Stack(256)

while program[i] != "END":
    opcode = program[i]
    i += 1

    if opcode == "PUSH":
        stack.push(program[i])
        i += 1
    elif opcode == "POP":
        stack.pop()
    elif opcode == "ADD":
        a, b = stack.pop(), stack.pop()
        stack.push(a+b)
    elif opcode == "SUBTRACT":
        a, b = stack.pop(), stack.pop()
        stack.push(b-a)
    elif opcode == "LOG":
        string_literal = program[i]
        i += 1
        print(string_literal)
    elif opcode == "READ":
        number = int(input())
        stack.push(number)
    elif opcode == "IF_0_GOTO":
        number = stack.top()
        if number == 0:
            i = label_tracker[program[i]]
        else:
            i += 1
    elif opcode == "IF_GT_0_GOTO":
        number = stack.top()
        if number > 0:
            i = label_tracker[program[i]]
        else:
            i += 1
