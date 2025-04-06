import os
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
pc = 0 # Program counter
pointer = 1

memory[pointer] += 1

brainfuck_program = open(args.brainfuck_program_name, "r")

while True:
    try:
        memory[pointer] += 1
        pc += 1
        pointer += 1
    except IndexError:
        pointer -= 1