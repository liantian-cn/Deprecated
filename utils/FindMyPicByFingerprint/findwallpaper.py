#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'Liantian'
# __email__ = "liantian.me+code@gmail.com"
#
# MIT License
#
# Copyright (c) 2018 liantian
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import sys
from optparse import OptionParser
from PIL import Image
from shutil import copy
from main import get_image_files, progress, img_hash
import ctypes

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def find_wallpaper(best_width, best_height, work_dir):
    best_resolution_dir = os.path.join(os.path.dirname(work_dir), '{0}x{1}_equal'.format(best_width, best_height))
    larger_resolution_dir = os.path.join(os.path.dirname(work_dir), '{0}x{1}_larger'.format(best_width, best_height))
    if not os.path.exists(best_resolution_dir):
        os.makedirs(best_resolution_dir)
    if not os.path.exists(larger_resolution_dir):
        os.makedirs(larger_resolution_dir)
    pictures = get_image_files(work_dir)
    count = 0
    total = len(pictures)
    for img_file in pictures:
        progress(count, total)
        count += 1
        image = Image.open(img_file["file"])
        try:
            fp1, fp2, width, height = img_hash(image)
            if (width == int(best_width)) and (height == int(best_height)):
                copy(img_file["file"], os.path.join(best_resolution_dir,
                                                    "{0}_{1}_{2}{3}".format(img_file["folder"],
                                                                            img_file["basename"],
                                                                            fp2,
                                                                            img_file["extension"])
                                                    ))
            elif (width >= int(best_width)) and (height >= int(best_height)):
                copy(img_file["file"], os.path.join(larger_resolution_dir,
                                                    "{0}_{1}_{2}{3}".format(img_file["folder"],
                                                                            img_file["basename"],
                                                                            fp2,
                                                                            img_file["extension"])
                                                    ))
        except OSError as e:
            print(img_file["file"], e)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("--best-width",
                      help="Best Width, The current default is {0}".format(user32.GetSystemMetrics(0)),
                      dest="best_width", default=user32.GetSystemMetrics(0))
    parser.add_option("--best-height",
                      help="Best Height, The current default is {0}".format(user32.GetSystemMetrics(1)),
                      dest="best_height", default=user32.GetSystemMetrics(1))
    parser.add_option("--dir", help="Dir, The current default is {0}".format(os.getcwd()), dest="work_dir",
                      default=os.getcwd())
    (options, args) = parser.parse_args()
    if os.path.normpath(os.path.dirname(options.work_dir)) == os.path.normpath(options.work_dir):
        print("can not set path equal driver root")
        sys.exit(0)

    find_wallpaper(best_width=options.best_width,
                   best_height=options.best_height,
                   work_dir=options.work_dir)

