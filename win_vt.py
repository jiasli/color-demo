# Source: https://bugs.python.org/issue30075

import ctypes
import msvcrt
import os
from ctypes import wintypes


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
