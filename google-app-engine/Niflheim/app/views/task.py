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

from main import app
from models import Post, Category, Archive


# from models import Comment


@app.route('/task/category_count', methods=['GET'], endpoint="task.category_count")
def category_count():
    queue = []
    queue2 = []
    categories = Category.query().fetch()
    for c in categories:
        cq = dict({})
        cq["object"] = c
        if c.parent is None:
            cq["c_future"] = Category.query(Category.parent == c.key).count_async()
        cq["p_future"] = Post.query(Post.category == c.key, Post.status == Post.STATUS_PUBLISHED).count_async()
        queue.append(cq)

    for q in queue:
        c = q["object"]
        c.post_count = q["p_future"].get_result()
        if q.get("c_future", False):
            c.child_count = q["c_future"].get_result()
        else:
            c.child_count = 0
        queue2.append(c.put_async())

    for q in queue2:
        q.get_result()
    return "Done"


@app.route('/task/archive_count', methods=['GET'], endpoint="task.archive_count")
def archive_count():
    queue = []
    queue2 = []
    archives = Archive.query().fetch()
    for archive in archives:
        cq = dict({})
        cq["object"] = archive
        cq["p_future"] = Post.query(Post.archive == archive.key, Post.status == Post.STATUS_PUBLISHED).count_async()
        queue.append(cq)

    for q in queue:
        c = q["object"]
        c.post_count = q["p_future"].get_result()
        queue2.append(c.put_async())

    for q in queue2:
        q.get_result()
    return "Done"
