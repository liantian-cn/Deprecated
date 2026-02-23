#!/usr/bin/env python27
# -*- coding: utf-8 -*-
# __author__ = 'Liantian'
# __email__ = "liantian.me+code@gmail.com"
#
# Copyright 2015-2016 liantian
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org>

from __future__ import print_function
import ctypes
import ctypes.wintypes
import random
import time


"""

https://msdn.microsoft.com/en-us/library/windows/desktop/aa373208(v=vs.85).aspx

"""

ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002


def sleep_enable():
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)


def sleep_disable():
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED)


def get_cursor_pos():
    obj_point = ctypes.wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(obj_point))
    return obj_point.x, obj_point.y


def set_cursor_pos(x=0, y=0):
    return ctypes.windll.user32.SetCursorPos(x, y)


def random_move_cursor():
    cur_x, cur_y = get_cursor_pos()
    set_cursor_pos(cur_x + random.randint(-1, 1), cur_y + random.randint(-1, 1))


if __name__ == "__main__":
    sleep_disable()
    i = 0
    p = ['|', '/', '-', '\\']
    while True:
        print('\r' + p[i % 4], end="")
        time.sleep(5)
        random_move_cursor()
        i += 1
