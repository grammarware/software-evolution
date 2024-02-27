#!/usr/local/bin/python3.12
import os
import sys

SEVEN = ' ' * 7
ELEVEN = ' ' * 11
KEYWORDS = ('ACCEPT', 'ADD', 'ALTER', 'CALL', 'COPY', 'DISPLAY', 'DIVIDE', 'EVALUATE', 'GO', 'IF', 'LOOP', 'MOVE', 'MULTIPLY',
    'NEXT', 'PERFORM', 'PERFORM', 'SIGNAL', 'STOP', 'SUBTRACT', )

# Split the input on spaces, unless they are within double quotes
def split_into_tokens(contents):
    tokens = []
    quoted = False
    current_token = ''
    for char in contents:
        if char == '"':
            quoted = not quoted
            current_token += char
        elif char == ' ' and not quoted:
            tokens.append(current_token)
            current_token = ''
        else:
            current_token += char
    if current_token:
        tokens.append(current_token)
    return tokens

def glue(line, token):
    if line:
        return line + ' ' + token
    else:
        return token

def writeX(indent, line, write_proc):
    line_to_write = indent + line
    cont_indent = indent[:6] + '-' + indent[7:]
    while len(line_to_write) > 72:
        write_proc(line_to_write[:72] + '\n')
        line_to_write = cont_indent + line_to_write[72:]
    if line_to_write:
        write_proc(line_to_write + '\n')

def gen_writeA(write_proc):
    global SEVEN
    return lambda line: writeX(SEVEN, line, write_proc)

def gen_writeB(write_proc):
    global ELEVEN
    return lambda line: writeX(ELEVEN, line, write_proc)

def format_tokens(write, tokens):
    global KEYWORDS
    writeA = gen_writeA(write)
    writeB = gen_writeB(write)
    line = ''
    division = next_division = '?'
    even = 0
    for token in tokens:
        if token == 'DIVISION':
            if line.endswith('IDENTIFICATION'):
                next_division = 'I'
            elif line.endswith('DATA'):
                next_division = 'D'
            elif line.endswith('PROCEDURE'):
                next_division = 'P'
            else:
                print('ERROR: unknown division: ' + line.split()[-1])
            line = glue(line, token)
            continue
        if division == '?':
            if token == '.':
                line += token
                writeA(line)
                line = ''
            else:
                line = glue(line, token)
        elif division == 'I':
            # IDENTIFICATION DIVISION
            if token == '.':
                even += 1
                if next_division != 'I':
                    line += token
                    writeA(line)
                    line = ''
                elif even % 2 == 0:
                    line += token
                    writeB(line)
                    line = ''
                else:
                    line += token
            else:
                line = glue(line, token)
        elif division == 'D':
            if token == '.':
                line += token
                writeA(line)
                line = ''
            else:
                line = glue(line, token)
        elif division == 'P':
            if not line:
                first = True
                line = token
                continue
            if first:
                if line not in KEYWORDS:
                    if token == '.':
                        writeA(line + token)
                        line = ''
                    else:
                        # paragraph name without a period => weird!
                        writeA(line)
                        line = token
                else:
                    line = glue(line, token)
                first = False
                continue
            if token in KEYWORDS:
                writeB(line)
                line = token
            elif token == '.':
                line += token
                writeB(line)
                line = ''
            else:
                line = glue(line, token)
        else:
            print('Unknown division code ' + division)
        division = next_division

# Process one BabyCobol file
def process_file(input_folder, output_folder, filename):
    input_filename  = os.path.join(input_folder, filename)
    output_filename = os.path.join(output_folder, filename)
    with open(input_filename, 'r') as file:
        tokens = split_into_tokens(file.read())
    with open(output_filename, 'w') as file:
        format_tokens(file.write, tokens)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: ./formatter.py input_folder output_folder')
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    if not os.path.isdir(input_folder):
        print(f'Error: {input_folder} is not a directory')
        sys.exit(1)
    if not os.path.isdir(output_folder):
        print(f'Error: {output_folder} is not a directory')
        sys.exit(1)

    cx = 0
    for filename in os.listdir(input_folder):
        if filename.endswith('.baby'):
            cx += 1
            process_file(input_folder, output_folder, filename)
        if cx % 10000 == 0:
            print(f'{cx}th file is {filename}')
