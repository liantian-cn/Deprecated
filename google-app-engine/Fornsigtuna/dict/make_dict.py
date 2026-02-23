#!/usr/bin/env python2
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

import io
import re
import marshal

BASE_S2T_DICT = ["STCharacters.txt", "STPhrases.txt"]
BASE_T2S_DICT = ["TSCharacters.txt", "TSPhrases.txt"]


def make_dict(name, base_dict_file=[], rev_dict_file=[]):
    tran_dict = dict()
    for txt_dict in rev_dict_file:
        with io.open(txt_dict, mode="r", encoding="utf-8") as f:
            txt_lines = f.readlines()
            for txt_line in txt_lines:
                if not ((txt_line.strip() == "") or (txt_line.strip() == u"")):
                    dst, src = txt_line.split("\t", 1)
                    dst = dst.split(" ")[0]
                    src = src.strip()
                    dst = dst.strip()
                    tran_dict[src] = dst
    for txt_dict in base_dict_file:
        with io.open(txt_dict, mode="r", encoding="utf-8") as f:
            txt_lines = f.readlines()
            for txt_line in txt_lines:
                if not ((txt_line.strip() == "") or (txt_line.strip() == u"")):
                    src, dst = txt_line.split("\t", 1)
                    dst = dst.split(" ")[0]
                    src = src.strip()
                    dst = dst.strip()
                    tran_dict[src] = dst

    tran_list = []
    for key, value in tran_dict.iteritems():
        if key != value:
            tran_list.append((key, value))

    tran_list.sort(key=lambda item: (-len(item[0]), item))

    print(len(tran_list))
    Rep = dict((re.escape(k), v) for k, v in tran_list)
    Pattern_str = "|".join(Rep.keys())
    with open("{}.marshal".format(name), 'wb') as cf:
        marshal.dump((Rep, Pattern_str), cf)


if __name__ == '__main__':
    make_dict("hans-to-hant", base_dict_file=BASE_S2T_DICT, rev_dict_file=BASE_T2S_DICT)
    make_dict("hant-to-hans", base_dict_file=BASE_T2S_DICT, rev_dict_file=BASE_S2T_DICT)
    make_dict("hant-to-tw", base_dict_file=[
        "TWPhrasesIT.txt",
        "TWPhrasesName.txt",
        "TWPhrasesOther.txt",
        "TWVariants.txt",
        "TWVariantsRevPhrases.txt",
    ])
    make_dict("hant-to-hk", base_dict_file=[
        "HKVariantsRevPhrases.txt",
        "HKVariantsPhrases.txt",
        "HKVariants.txt",
    ])
    make_dict("tw-to-hant", rev_dict_file=[
        "TWPhrasesIT.txt",
        "TWPhrasesName.txt",
        "TWPhrasesOther.txt",
        "TWVariants.txt",
        "TWVariantsRevPhrases.txt",
    ])
    make_dict("hk-to-hant", rev_dict_file=[
        "HKVariantsRevPhrases.txt",
        "HKVariantsPhrases.txt",
        "HKVariants.txt",
    ])



    # q = dict()
    # for a in HANT_ZhConversion:
    #     q[a[0]] = a[1]
    # for b in ZhConversion:
    #     q[b[0]] = b[1]
    # e = []
    # for key, value in q.iteritems():
    #     e.append((key, value))
    # e.sort(key=lambda item: (-len(item[0]), item))
    # cache_file = "zh-tw.marshal"
    # Rep = dict((re.escape(k), v) for k, v in e)
    # Pattern_str = "|".join(Rep.keys())
    #
    # with open(cache_file, 'wb') as cf:
    #     marshal.dump((Rep, Pattern_str), cf)
