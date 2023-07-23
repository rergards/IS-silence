import argparse
import random
import os
import base64
import os
try:
    import tkinter as tk
except ImportError:
    tk = None

def roll_die(sides):
    return random.randint(1, sides)

def get_line_from_file(filename, line_num, encoded):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(script_dir, "tables", filename)
    with open(path, 'r') as file:
        if encoded:
            content = base64.b64decode(file.read()).decode('utf-8')
            lines = content.split('\n')
        else:
            lines = file.readlines()
        return lines[0], lines[line_num].strip()  # returning header and the line

def main(encoded):
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
            header, line = get_line_from_file(filename, roll, encoded)
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--encoded", help="Specify if files are base64 encoded", action="store_true")
    args = parser.parse_args()
    main(args.encoded)
