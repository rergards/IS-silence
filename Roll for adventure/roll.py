import argparse
import random
import os
import base64
import binascii
import logging

try:
    import tkinter as tk
except ImportError:
    tk = None

def roll_die(sides):
    """Roll a die with the given number of sides and return the result."""
    return random.randint(1, sides)

def get_line_from_file(filename, line_num):
    """
    Get the specified line from the file.

    If the file is base64 encoded, it is decoded first.
    If it's not base64, it is read as it is.
    """
    script_dir = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(script_dir, "tables", filename)
    try:
        with open(path, 'rb') as file:
            content = file.read()
            try:
                # Try to decode as base64
                content = base64.b64decode(content).decode('utf-8')
            except (binascii.Error, UnicodeDecodeError):
                # If it fails, it's not base64, so decode as plain text
                content = content.decode('utf-8')
    except Exception as e:
        logging.error(f"An error occurred while trying to read from file {filename}: {e}")
        raise

    lines = content.split('\n')
    return lines[0], lines[line_num].strip()  # returning header and the line

def main():
    """Main function that performs the dice rolls and prints the results."""
    dice_to_roll = {
        '100': 4,
        '30': 3,
        '10': 1
    }
    filenames = {
        '100': '100',
        '30': ['30-1', '30-2', '30-3'],
        '10': '10'
    }
    output = []
    for sides, quantity in dice_to_roll.items():
        results = []
        headers = []
        for _ in range(quantity):
            roll = roll_die(int(sides))
            if sides == '30':
                filename = random.choice(filenames[sides])
            else:
                filename = filenames[sides]
            header, line = get_line_from_file(filename, roll)
            headers.append(header)
            results.append(line)
            output.append(f'Rolled a {sides} sided die, result: {roll}')
        if sides == '100':
            output.append(f"{headers[0]}: {', '.join(results)}")
        else:
            for header, result in zip(headers, results):
                output.append(f"{header}: {result}")

    output_str = '\n'.join(output)
    if 'DISPLAY' in os.environ and tk is not None:
        root = tk.Tk()
        text = tk.Text(root)
        text.insert(tk.INSERT, output_str)
        text.pack()
        tk.mainloop()
    else:
        print(output_str)

if __name__ == '__main__':
    main()
