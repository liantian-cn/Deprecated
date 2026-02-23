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

import datetime
import json

from google.appengine.api import memcache

from main import app
from models import Post, Category, Archive


# from models import Comment


# @app.context_processor
# def config_processor():
#     return dict(site_config=app.config)


@app.context_processor
def datetime_processor():
    return dict(now=datetime.datetime.now())


@app.context_processor
def page_processor():
    mem = memcache.get('PAGES')
    if mem is None:
        pages = []
        ps = Post.query(Post.status == Post.STATUS_PAGE).order(Post.order).fetch()
        for p in ps:
            pages.append({"title": p.title, "slug": p.slug})
        memcache.add(key="PAGES", value=json.dumps(pages, encoding="utf-8"), time=app.config["SITE_MEMCACHED_TIME"])
    else:
        pages = json.loads(mem, encoding="utf-8")

    return dict(pages=pages)


@app.context_processor
def recent_post_processor():
    if app.config["SITE_SIDEBAR_SHOW_RECENT_POST"]:
        mem = memcache.get('RECENT_POST')
        if mem is None:
            recent_post = []
            for p in Post.query(Post.status == Post.STATUS_PUBLISHED).order(-Post.modified).fetch(limit=app.config["SITE_SIDEBAR_RECENT_POST_NUM"]):
                recent_post.append({"title": p.title, "slug": p.slug})
            memcache.add(key="RECENT_POST", value=json.dumps(recent_post, encoding="utf-8"), time=app.config["SITE_MEMCACHED_TIME"])
        else:
            recent_post = json.loads(mem, encoding="utf-8")
    else:
        recent_post = []

    return dict(recent_post=recent_post)


# @app.context_processor
# def recent_comment_processor():
#     if app.config["SITE_SIDEBAR_SHOW_RECENT_COMMENT"]:
#         mem = memcache.get('RECENT_COMMENT')
#         if mem is None:
#             recent_comment = []
#             for c in Comment.query().order(-Comment.created).fetch(limit=app.config["SITE_SIDEBAR_RECENT_COMMENT_NUM"]):
#                 recent_comment.append({"nickname": c.nickname, "text": c.text, "key": c.post.urlsafe()})
#             memcache.add(key="RECENT_COMMENT", value=json.dumps(recent_comment, encoding="utf-8"), time=app.config["SITE_MEMCACHED_TIME"])
#         else:
#             recent_comment = json.loads(mem, encoding="utf-8")
#     else:
#         recent_comment = []
#
#     return dict(recent_comment=recent_comment)


@app.context_processor
def categories_processor():
    if app.config["SITE_SIDEBAR_SHOW_CATEGORY"]:
        mem = memcache.get('CATEGORIES')
        if mem is None:
            categories = []
            lv_1 = {}
            cs = Category.query().fetch()
            for c in cs:
                if c.parent is None:
                    lv_1[c.key.urlsafe()] = {"title": c.title, "post_count": c.post_count, "slug": c.slug, "child": []}
            for c in cs:
                if c.parent is not None:
                    lv_1[c.parent.urlsafe()]["child"].append({"title": c.title, "slug": c.slug, "post_count": c.post_count})
            for k, v in lv_1.iteritems():
                categories.append(v)
            memcache.add(key="CATEGORIES", value=json.dumps(categories, encoding="utf-8"), time=app.config["SITE_MEMCACHED_TIME"])
        else:
            categories = json.loads(mem, encoding="utf-8")
    else:
        categories = []
    return dict(categories=categories)


@app.context_processor
def archive_processor():
    if app.config["SITE_SIDEBAR_SHOW_ARCHIVE"]:
        mem = memcache.get('ARCHIVES')
        if mem is None:
            archives = []
            for archive in Archive.query().order(Archive.time).fetch():
                archives.append({
                    "post_count": archive.post_count,
                    "year": archive.time.strftime("%Y"),
                    "month": archive.time.strftime("%m"),
                    "format_time": archive.time.strftime(app.config["SITE_SIDEBAR_ARCHIVE_DATE_FORMAT"])
                })
            memcache.add(key="ARCHIVES", value=json.dumps(archives, encoding="utf-8"), time=app.config["SITE_MEMCACHED_TIME"])
        else:
            archives = json.loads(mem, encoding="utf-8")
    else:
        archives = []
    return dict(archives=archives)
