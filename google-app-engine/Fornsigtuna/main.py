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

import marshal
import re

from flask import Flask, request, jsonify, make_response, render_template


class Translator(object):
    def __init__(self, rep, pattern):
        self.rep = rep
        self.pattern = pattern

    def translation(self, text):
        return self.pattern.sub(lambda m: self.rep[re.escape(m.group(0))], text)


def read_dict(file_name):
    with open(file_name, 'rb') as cf:
        rep, pattern_str = marshal.load(cf)
        pattern = re.compile(pattern_str)
    return Translator(rep, pattern)


dict_hans_to_hant = read_dict("dict/hans-to-hant.marshal")
dict_hant_to_hans = read_dict("dict/hant-to-hans.marshal")
dict_hant_to_hk = read_dict("dict/hant-to-hk.marshal")
dict_hant_to_tw = read_dict("dict/hant-to-tw.marshal")
dict_hk_to_hant = read_dict("dict/hk-to-hant.marshal")
dict_tw_to_hant = read_dict("dict/tw-to-hant.marshal")

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return "Error : 404 - Page Not Found", 404


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/api', methods=['POST'])
def api():
    text = request.values.get('text', "parameter 'text' is empty\n")
    lang = request.values.get('lang', "parameter 'lang' is empty\n")
    html = request.values.get('html', False)

    lang = lang.decode("utf-8").lower()
    if not (lang in (u"zh-hans", u"zh-cn", u"zh-tw", u"zh-hk", u"zh-hant")):
        response = make_response(jsonify(error="parameter 'lang' is error\n"))
        return response

    if isinstance(text, str):
        text = text.decode("utf-8")
    if not isinstance(text, unicode):
        response = make_response(jsonify(error="text is not utf-8 encode\n"))
        return response
    src_text = text
    if lang == u"zh-hans":
        text = dict_hant_to_hans.translation(text)
    elif lang == u"zh-hant":
        text = dict_hans_to_hant.translation(text)
    elif lang == u"zh-cn":
        text = dict_hk_to_hant.translation(text)
        text = dict_tw_to_hant.translation(text)
        text = dict_hant_to_hans.translation(text)
    elif lang == u"zh-hk":
        text = dict_hans_to_hant.translation(text)
        text = dict_hant_to_hk.translation(text)
    elif lang == u"zh-tw":
        text = dict_hans_to_hant.translation(text)
        text = dict_hant_to_tw.translation(text)
    else:
        text = text

    if not bool(html):
        response = make_response(jsonify(result=text, lang=lang, text=src_text, html=bool(html)))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
        return response
    else:
        return render_template("result.html", result=text)
