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


from google.appengine.ext import ndb


class Post(ndb.Model):
    site_name = ndb.TextProperty(verbose_name=u"站點名稱", required=True, indexed=False)
    author = ndb.TextProperty(verbose_name=u"作者", required=True, indexed=False)
    domain = ndb.TextProperty(verbose_name=u"域名", required=True, indexed=False)
    text = ndb.TextProperty(verbose_name=u"内容文字", required=True, indexed=False)

    @property
    def clean_domain(self):
        return self.domain.encode("utf-8")


class Attachment(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True, indexed=False)
    file = ndb.BlobProperty(compressed=True, indexed=False)
    filename = ndb.StringProperty(indexed=False)
    mime_type = ndb.StringProperty(indexed=False)

