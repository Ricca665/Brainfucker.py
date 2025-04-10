import requests
import logging
import argparse
import re
import sys

logging.basicConfig(level=logging.DEBUG)

def main(args, memory, pointer):
    try:
        brainfuck_program = open(args.brainfuck_program_name, "r")     
    except FileNotFoundError:
        print("ERROR: File not found!")
        sys.exit(1)

    brainfuck_program = brainfuck_program.read()
    run_program(brainfuck_program, memory, pointer)

def run_program(brainfuck_program, memory, pointer):
    """Runs the brainfuck program"""
    pc = 0 # Program counter
    temp_stack = []
    bracemap = {}

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
                print(chr(memory[pointer])) # Converts the current cell to ascii and prints it
            elif i == "_":
                print(memory[pointer]) # Like the . but it doesn't convert the number to ascii, useful for debugging
            elif i == ",":
                value = ord(str(input()[0]))
                try:
                    memory[pointer] = value
                except Exception:
                    pass
            elif i == "[":
                if memory[pointer] == 0:
                    pc = bracemap[pc]  # Jump to matching "]" if current cell is 0
                    continue # We don't aumentate the program counter, fixing loops overall

            elif i == "]":
                if memory[pointer] != 0:
                    pc = bracemap[pc]  # Jump to matching "[" if current cell is non-zero

            elif i == "n": # GET requests
                url = re.search(r'g(https?://[^\s]+)G', brainfuck_program) # Grab the url between g and G
                if url:
                    url = url.group(1) # Grab it as a string, but just first match
                    url_code = requests.get(url) # Does the request
                    pc = len(url)-1
                    url_code = url_code.status_code # Gets the status code
                    memory[pointer] = url_code # Puts the status code in the current memory pointer
                else:
                    pass

            elif i == "p": # POST requests
                url = re.search(r'g(https?://[^\s]+)G', brainfuck_program) # Grab the url between g and G
                if url:
                    url = url.group(1) # Grab it as a string, but just first match
                    url_code = requests.post(url) # Does the request
                    pc = len(url)-1
                    url_code = url_code.status_code # Gets the status code
                    memory[pointer] = url_code # Puts the status code in the current memory pointer
                    logging.debug(url_code)
                    logging.debug(url)
                else:
                    pass

            if args.verbose: #Debug
                logging.debug(memory[pointer])

            pc += 1


    except IndexError: # In case the fucking pointer exits
        pointer -= 1 # Reduce our pointer
    except Exception as e: # Ignore any python exception
        if args.verbose:
            logging.debugging(f"The unexpected error that wasn't expected was expected: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        prog='Brainfucker.py++',
                        description='Brainfuck interpreter for python, with extra feaures',
                        epilog="""It's fucking my brain up help""")

    parser.add_argument('brainfuck_program_name')
    parser.add_argument('-v', '--verbose',
                        action='store_true')
    parser.add_argument('-b', '--blocks')
    args = parser.parse_args()


    memory = [0] * 30000 # 30000 memory cells
    pointer = 0

    if args.blocks:
        memory = None
        try:
            memory = [0]*int(args.blocks)
        except Exception: # In case it's invalid
            memory = [0]*30000 # Set it to default 
    if not args.verbose:
        logging.getLogger("urllib3").setLevel(logging.WARNING)

    main(args, memory, pointer)
