#!/usr/bin/env python3
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
# For more information, please refer to <https://unlicense.org>

import logging
import configparser
import socket
from threading import Thread
import pickle
import pyautogui
import ctypes

config = configparser.ConfigParser()
config.read('config.ini')
logging.basicConfig(format='%(asctime)s [%(levelname)s]  %(message)s', level=logging.DEBUG)


class KeyServer(Thread):
    def __init__(self, sock, address):
        Thread.__init__(self)
        self.sock = sock
        self.address = address

    def run(self):
        with self.sock:
            logging.info('Connected by {0}'.format(self.address))
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                data = pickle.loads(data)
                dst_key = data.get("DST", None)
                if dst_key is not None:
                    logging.info('Press {0}'.format(dst_key))
                    pyautogui.press(dst_key)


if __name__ == '__main__':
    if not ctypes.windll.shell32.IsUserAnAdmin():
        logging.warn("script run as user permissions")
    host = "0.0.0.0"
    port = int(config["DEFAULT"]["port"])
    logging.info('Listen on:  {0}:{1}'.format(host, port))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        while True:
            conn, address = s.accept()
            KeyServer(conn, address).start()
