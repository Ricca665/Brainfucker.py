
import logging
import argparse
logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser(
                    prog='Brainfucker.py',
                    description='Brainfuck interpreter for python',
                    epilog="""It's fucking my brain up help""")

parser.add_argument('brainfuck_program_name')
parser.add_argument('-v', '--verbose',
                    action='store_true')

args = parser.parse_args()

memory = [0] * 30000 # 30000 memory cells
pointer = 0

memory[pointer] += 1
pc = 0 # Just used in loops

temp_stack = []
bracemap = {}

brainfuck_program = open(args.brainfuck_program_name, "r")
brainfuck_program = brainfuck_program.read()

"""We need to check for each [ it's maching ]"""
for pos, char in enumerate(brainfuck_program):
    if char == "[":
        temp_stack.append(pos)
    elif char == "]":
        start = temp_stack.pop()
        bracemap[start] = pos
        bracemap[pos] = start

try:
    while pc < len(brainfuck_program): # While program counter is less than the lenght of the program
        i = brainfuck_program[pc] # store the current instruction in i

        """Evaluation of each instructions"""
        if i == "+":
            memory[pointer] += 1
        elif i == "-":
            memory[pointer] -= 1
        elif i == ">":
            if pointer < 30000:
                pointer += 1
        elif i == "<":
            if pointer > 0:
                pointer -= 1
        elif i == ".":
            print(str(memory[pointer]))
        elif i == ",":
            value = ord(str(input()[0]))
            try:
                memory[pointer] = value
            except Exception:
                pass
        elif i == "[":
            if memory[pointer] == 0:
                pc = bracemap[pc]  # Jump to matching "]" if current cell is 0
        elif i == "]":
            if memory[pointer] != 0:
                pc = bracemap[pc]  # Jump to matching "[" if current cell is non-zero

        if args.verbose: #Debug
            logging.debug(memory[pointer])
        
        pc += 1

except IndexError: # In case the fucking pointer exits
    pointer -= 1 # Reduce our pointer
except Exception: # Ignore any python exception
    pass