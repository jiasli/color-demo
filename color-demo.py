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


def print_rgb(text, rgb):
    esc = '\x1b[38;2;{};{};{}m'.format(*rgb)
    esc_reset = '\x1b[0m'
    print(esc + text + esc_reset, end='')


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
    print("🎃👻🦉🧙‍🔮✓⦿⦾测试テスト")

    # Print text in the basic 16 colors
    for color in COLORS:
        text = "This is some text in {:14s} {:8s}  █████████████████".format(
            color, COLORS[color].replace('\x1b', '\\x1b'))
        colored_text = COLORS[color] + text + DEFAULT
        print("{:14s}: {}".format(color, colored_text))

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
