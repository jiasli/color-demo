import colorsys
import os
import sys

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


def print_block(rgb):
    print_rgb("█", rgb)


def main():
    if 'vt' in sys.argv:
        if os.name == 'nt':
            from win_vt import enable_vt_mode
            enable_vt_mode()

    if 'text' in sys.argv:
        # Print text in the 16 basic colors

        # 🎃👻🦉🧙‍🔮: some emoji
        # ✓: https://www.compart.com/en/unicode/U+2713
        # ⦿: https://www.compart.com/en/unicode/U+29BF
        # ⦾: https://www.compart.com/en/unicode/U+29BE
        # 测试: "test" in Chinese
        # テスト: "test" in Japanese
        print("Test Unicode: 🎃👻🦉🧙‍🔮✓⦿⦾测试テスト")

        for color in COLORS:
            text = "This is some text in {:14s} {:8s}  █████████████████".format(
                color, COLORS[color].replace('\x1b', '\\x1b'))
            colored_text = COLORS[color] + text + DEFAULT
            print("{:14s}: {}".format(color, colored_text))

    if 'table' in sys.argv:
        # Print text in the 256 color table
        base = 16
        print("  0~ 15 ", end='')
        for i in range(base):
            print_color_index("█", i)
        print()
        row = 6
        column = 36
        for i in range(0, row):
            start = base + i * column
            end = base + i * column + column - 1
            print(f"{start:3d}~{end:3d} ", end='')
            for j in range(0, column):
                print_color_index("█", start + j)
            print()
        print("232~255 ", end='')
        for i in range(232, 256):
            print_color_index("█", i)
        print()

    if 'hsv' in sys.argv:
        # Draw HSV map dominated by h
        for h in range(11):
            for v in range(21):
                for s in range(51):
                    rgb = tuple(int(255 * x) for x in colorsys.hsv_to_rgb(h/10, s/50, 1-v/20))
                    print_block(rgb)
                print()

    if 'hsv-v' in sys.argv:
        # Draw HSV map dominated by v
        for v in range(11):
            for s in range(21):
                for h in range(101):
                    rgb = tuple(int(255 * x) for x in colorsys.hsv_to_rgb(1-h/100, 1-s/20, v/10))
                    print_block(rgb)
                print()

    if 'hsv-v-full' in sys.argv:
        # Draw HSV map with full v
        v = 1
        for s in range(21):
            for h in range(101):
                rgb = tuple(int(255 * x) for x in colorsys.hsv_to_rgb(1-h/100, 1-s/20, v))
                print_block(rgb)
            print()

    if 'rgb' in sys.argv:
        # Draw RGB map
        def _iter_to_ff(step):
            for value in range(0, 0xff, step):
                yield value
            yield 0xff

        for r in _iter_to_ff(0x10):
            # Print r label
            print(f'\x1b[38;2;255;0;0m{r:02x} ', end='')

            # Print b label
            b_label = ['{:4s}'.format('{:02x}'.format(b)) for b in _iter_to_ff(0x10)]
            print('\x1b[38;2;0;0;255m' + ''.join(b_label))

            for g in _iter_to_ff(0x10):
                # Print g label
                print(f'\x1b[38;2;0;255;0m{g:02x} ', end='')
                for b in _iter_to_ff(0x4):
                    print_block((r, g, b))
                print()
            print()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.argv.extend(['text', 'hsv-v-full'])
    main()
