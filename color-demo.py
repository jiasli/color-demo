import colorsys
import ctypes
import msvcrt
import os
from ctypes import wintypes

import numpy

DEFAULT = '\x1b[0m'

COLORS = {
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

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

ERROR_INVALID_PARAMETER = 0x0057
ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004


def _check_bool(result, func, args):
    if not result:
        raise ctypes.WinError(ctypes.get_last_error())
    return args


LPDWORD = ctypes.POINTER(wintypes.DWORD)
kernel32.GetConsoleMode.errcheck = _check_bool
kernel32.GetConsoleMode.argtypes = (wintypes.HANDLE, LPDWORD)
kernel32.SetConsoleMode.errcheck = _check_bool
kernel32.SetConsoleMode.argtypes = (wintypes.HANDLE, wintypes.DWORD)


def set_conout_mode(new_mode, mask=0xffffffff):
    # don't assume StandardOutput is a console.
    # open CONOUT$ instead
    fdout = os.open('CONOUT$', os.O_RDWR)
    try:
        hout = msvcrt.get_osfhandle(fdout)
        old_mode = wintypes.DWORD()
        kernel32.GetConsoleMode(hout, ctypes.byref(old_mode))
        print('old_mode={:08b}'.format(old_mode.value))
        if old_mode.value & mask:
            print('Virtual Terminal is already turned on.')
        else:
            print('Turning on Virtual Terminal.')
            mode = (new_mode & mask) | (old_mode.value & ~mask)
            print('new_mode={:08b}'.format(mode))
            kernel32.SetConsoleMode(hout, mode)
        return old_mode.value
    finally:
        os.close(fdout)


def enable_vt_mode():
    mode = mask = ENABLE_VIRTUAL_TERMINAL_PROCESSING
    try:
        return set_conout_mode(mode, mask)
    except WindowsError as e:
        if e.winerror == ERROR_INVALID_PARAMETER:
            raise NotImplementedError
        raise


def print_rgb(text, rgb):
    esc = '\x1b[38;2;{};{};{}m'.format(*rgb)
    esc_reset = '\x1b[0m'
    print(esc + text + esc_reset, end='')


def main():
    enable_vt_mode()

    # Print some emoji
    print("🎃👻🦉🧙‍🔮")

    # Print text in the basic 16 colors
    for color in COLORS:
        text = "This is some text in {} {}. Please compare it in different terminals.".format(
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
