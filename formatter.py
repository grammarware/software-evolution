#!/usr/local/bin/python3.12
import os
import sys

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

def format_tokens(write, tokens):
    SEVEN = ' ' * 7
    ELEVEN = ' ' * 11
    writeA = lambda t: write(SEVEN  + t + '\n')
    writeB = lambda t: write(ELEVEN + t + '\n')
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
