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
import keyboard
import socket
import configparser
import pickle

logging.basicConfig(format='%(asctime)s [%(levelname)s]  %(message)s', level=logging.DEBUG)
config = configparser.ConfigParser()
config.read('config.ini')

key_map = dict()


def send_key(event):
    src_key = event.scan_code
    dst_key = key_map.get(event.scan_code, None)
    if dst_key is None:
        logging.info("SRC: {0:^6} Not find in key_map".format(src_key))
    else:
        try:
            sock = socket.socket()
            sock.settimeout(0.05)
            sock.connect((config["DEFAULT"]["host"], int(config["DEFAULT"]["port"])))
            sock.send(pickle.dumps({'SRC': src_key, 'DST': dst_key}))
            sock.close()
            logging.info("SENT KEY SRC: {0:^6} , DST: {1:^6}".format(src_key, dst_key))
        except ConnectionRefusedError:
            logging.error("Server Connet Error")
        except socket.timeout:
            logging.error("Server Connet Error")


def init():
    for key in config:
        if key.strip().lower().startswith("bind_"):
            q = key.strip().lower().split("_", 1)
            if len(q) < 2:
                continue
            src_key = int(q[1])
            dst_key = config[key]['destination']
            key_map[src_key] = dst_key
            keyboard.on_press_key(src_key, send_key)
            logging.info("ADD KEY MAP SRC: {0:^6} , DST: {1:^6}".format(src_key, dst_key))


if __name__ == '__main__':
    init()
    keyboard.wait()
