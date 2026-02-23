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
from PIL import Image



def img_hash(image, deviation=8):
    """
    :param image: 一个PIL图片对象。
    :param deviation: 误差值，默认是8
    :return: fp,seq 分别是指纹的字符串和序列格式

    """

    width = image.size[0]
    height = image.size[1]

    image = image.resize((deviation, deviation), Image.ANTIALIAS)
    # 第一步，缩小尺寸。
    # 将图片缩小到8x8的尺寸，总共64个像素。这一步的作用是去除图片的细节，只保留结构、明暗等基本信息，摒弃不同尺寸、比例带来的图片差异。

    image = image.convert(mode="L", colors=64)
    # 第二步，简化色彩。
    # 将缩小后的图片，转为64级灰度。也就是说，所有像素点总共只有64种颜色。

    color_seq = list(image.getdata())
    color_avg = sum(color_seq) / len(color_seq)
    # 第三步，计算平均值。计算所有64个像素的灰度平均值。

    result_seq = list(map(lambda x: 0 if x < color_avg else 1, [y for y in color_seq]))
    # 第四步，比较像素的灰度。
    # 将每个像素的灰度，与平均值进行比较。大于或等于平均值，记为1；小于平均值，记为0。

    fp1 = "".join(str(x) for x in result_seq)
    # fp1: 将像素比较结果直接连接为字符串
    fp2 = format(int("".join(str(x) for x in result_seq), base=2), "x")
    # fp2: 将fp1的字符串进行二进制>十六进制转换

    return fp1, fp2, width, height


def hamming(s1, s2):
    """得到指纹以后，就可以对比不同的图片，看看64位中有多少位是不一样的。在理论上，这等同于计算"汉明距离"（Hamming distance）。
    如果不相同的数据位不超过5，就说明两张图片很相似；如果大于10，就说明这是两张不同的图片。"""
    assert len(s1) == len(s2)
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))


def get_image_files(work_dir=os.getcwd()):
    """找到指定目录下所有的图片"""
    pictures = []
    ext_name = ('jpg', "jpeg", 'bmp', 'png', 'gif')
    for root, dirnames, fns in os.walk(work_dir):
        for fn in fns:
            if fn.lower().endswith(ext_name):
                img_file = os.path.join(root, fn)
                basename, extension = os.path.splitext(fn)
                pictures.append({"file": img_file,
                                 "root": root,
                                 "filename": fn,
                                 "basename": basename,
                                 "extension": extension,
                                 "folder": os.path.basename(root)})

    return pictures


def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()


