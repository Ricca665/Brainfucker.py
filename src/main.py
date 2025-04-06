
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

brainfuck_program = open(args.brainfuck_program_name, "r")
brainfuck_program = brainfuck_program.read()

try:
    for i in brainfuck_program:
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
            if memory[pointer] != 0:
                continue
        else:
            continue
        if args.verbose:
            logging.debug(memory[pointer])
            
except IndexError:
    pointer -= 1
    