import colorsys
import os

import numpy

DEFAULT = '\x1b[0m'

# https://docs.microsoft.com/en-us/windows/console/console-virtual-terminal-sequences
COLORS = {
    'default': '\x1b[0m',
    'black': '\x1b[30m',
    'red': '\x1b[31m',
    'green': '\x1b[32m',
    'yellow': '\x1b[33m',
    'blue': '\x1b[34m',
    'magenta': '\x1b[35m',
    'cyan': '\x1b[36m',
    'white': '\x1b[37m',
    'bright_black': '\x1b[90m',
    'bright_red': '\x1b[91m',
    'bright_green': '\x1b[92m',
    'bright_yellow': '\x1b[93m',
    'bright_blue': '\x1b[94m',
    'bright_magenta': '\x1b[95m',
    'bright_cyan': '\x1b[96m',
    'bright_white': '\x1b[97m',
}


def print_with_esc(text, esc):
    esc_reset = '\x1b[0m'
    print(esc + text + esc_reset, end='')


def print_rgb(text, rgb):
    print_with_esc(text, '\x1b[38;2;{};{};{}m'.format(*rgb))


def print_color_index(text, color_index):
    print_with_esc(text, '\x1b[38;5;{}m'.format(color_index))


def main():
    if os.name == 'nt':
        from win_vt import enable_vt_mode
        enable_vt_mode()

    # 🎃👻🦉🧙‍🔮: some emoji
    # ✓: https://www.compart.com/en/unicode/U+2713
    # ⦿: https://www.compart.com/en/unicode/U+29BF
    # ⦾: https://www.compart.com/en/unicode/U+29BE
    # 测试: "test" in Chinese
    # テスト: "test" in Japanese
    print("Test Unicode: 🎃👻🦉🧙‍🔮✓⦿⦾测试テスト")

    # Print text in the basic 16 colors
    for color in COLORS:
        text = "This is some text in {:14s} {:8s}  █████████████████".format(
            color, COLORS[color].replace('\x1b', '\\x1b'))
        colored_text = COLORS[color] + text + DEFAULT
        print("{:14s}: {}".format(color, colored_text))

    print()

    # Print text in the 256 color table
    base = 16
    print("  0~ 15 ", end='')
    for i in range(base):
        print_color_index("█", i)
    print()
    row = 6
    column = 36
    for i in range(0, row):
        print(f"{base + i * column:3d}~{base + i * column + column - 1:3d} ", end='')
        for j in range(0, column):
            print_color_index("█", base + i * column + j)
        print()
    print("232~255 ", end='')
    for i in range(232, 256):
        print_color_index("█", i)
    print()
    print()

    # Draw an HSV map
    v = 1
    for s in numpy.arange(1, 0, -0.05):
        for h in numpy.arange(0, 1, 0.01):
            rgb = tuple(int(255 * x) for x in colorsys.hsv_to_rgb(h, s, v))
            print_rgb("█", rgb)
            # print(rgb)
        print()


if __name__ == '__main__':
    main()
