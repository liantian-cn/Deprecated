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


import json
import logging
import urllib
from datetime import datetime

from google.appengine.api import memcache
from google.appengine.api import urlfetch
from slugify import slugify

from default_option import DEFAULT_OPTION
from main import app
from models import Option


def translate(text, source_lang="auto", target_lang="en"):
    url = 'https://translate.googleapis.com/translate_a/single?ie=UTF-8&client=gtx&sl={0}&tl={1}&dt=t&q={2}'
    request_url = url.format(source_lang.encode('utf-8'), target_lang.encode('utf-8'), urllib.quote(text.encode('utf-8')))
    logging.info("translate use url {}".format(request_url))
    result = urlfetch.fetch(request_url)
    if result.status_code == 200:
        data = json.loads(result.content)
        return data[0][0][0]
    else:
        logging.error("return code is not 200")
        raise LookupError("Error")


def pretty_slug(text):
    try:
        return slugify(translate(text))
    except:
        return slugify(text)


def init_option():
    mem = memcache.get('SITE_OPTIONS')

    if mem is None:
        cache_ops = {}
    else:
        cache_ops = json.loads(mem, encoding="utf-8")

    if set([opt["option"] for opt in DEFAULT_OPTION]) == set([key.encode("utf-8") for key, value in cache_ops.iteritems()]):
        for opt_name, opt_value in cache_ops.iteritems():
            app.config[opt_name.encode("utf-8")] = opt_value
        logging.info("load site option form memcache:{}".format(cache_ops))
    else:

        db_ops = {opt.key.id(): opt.value for opt in Option.query().fetch()}
        logging.info("load site option form db:{}".format(db_ops))
        cur_ops = {}
        for opt in DEFAULT_OPTION:
            opt_name = opt["option"]
            opt_default = opt["default_value"]
            opt_value = db_ops.get(opt_name, opt_default)
            app.config[opt_name] = opt_value
            cur_ops[opt_name] = opt_value
        memcache.add(key="SITE_OPTIONS", value=json.dumps(cur_ops, encoding="utf-8"), time=60 * 60)
    app.config["LATEST"] = datetime.now()


def int_to_str62(x):
    digit62 = 'KJlyinREahs8DUY0jobMLfqxHTBZuS29eIdFWw37ptA4kg6QcNz5PrC1XVOGvm'
    try:
        x = int(x)
    except:
        x = 0
    if x < 0:
        x = -x
    if x == 0:
        return "0"
    s = ""
    while x > 62:
        x1 = x % 62
        s = digit62[x1] + s
        x = x // 62
    if x > 0:
        s = digit62[x] + s
    return s


def time_id(start=datetime(2018, 1, 1)):
    return int_to_str62((datetime.now() - start).seconds)
