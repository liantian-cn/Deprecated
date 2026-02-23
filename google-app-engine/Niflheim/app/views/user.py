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

from datetime import date

import markdown
from flask import render_template, request
from google.appengine.api import search
from google.appengine.datastore.datastore_query import Cursor

from main import app
from models import Post, Category, Archive


# from models import Comment


@app.route('/', methods=['GET'], endpoint="index")
def index():
    cursor = request.args.get('cursor')
    start_cursor = Cursor(urlsafe=request.args.get('cursor'))
    posts, next_cursor, more = Post.query(Post.status == Post.STATUS_PUBLISHED).order(-Post.modified).fetch_page(page_size=app.config.get("SITE_POST_PER_PAGE"), start_cursor=start_cursor)
    return render_template('index.html',
                           posts=posts,
                           next_cursor=next_cursor,
                           cursor=cursor,
                           more=more)


@app.route('/search/', methods=['POST'], endpoint="search")
def post_search():
    query_string = request.form['s']
    results = search.Index('search-post').search(query_string)
    posts = []
    for item in results:
        posts.append({f.name: f.value for f in item.fields})
    return render_template('search.html',
                           query_string=query_string,
                           posts=posts)


@app.route('/post/<slug>/', methods=['GET'], endpoint="post")
@app.route('/page/<slug>/', methods=['GET'], endpoint="page")
def view_post(slug):
    post = Post.query(Post.slug == slug).fetch()[0]
    # comments = Comment.query(Comment.post == post.key).fetch()
    return render_template('post.html', post=post)


@app.route('/category/<slug>/', methods=['GET'], endpoint="category")
def category(slug):
    c = Category.query(Category.slug == slug).get()
    posts = Post.query(Post.category == c.key, Post.status == Post.STATUS_PUBLISHED).order(-Post.modified).fetch()
    return render_template('category.html', posts=posts, category=c)


@app.route('/archive/<year>/<month>/', methods=['GET'], endpoint="archive")
def archive(year, month):
    a = Archive.query(Archive.time == date(year=int(year), month=int(month), day=1)).get()
    posts = Post.query(Post.archive == a.key, Post.status == Post.STATUS_PUBLISHED).order(-Post.modified).fetch()
    return render_template('archive.html', posts=posts, archive=a)


@app.route('/pingback/', methods=['GET', 'POST'], endpoint="pingback")
def pingback():
    return render_template('index.html')


@app.route('/feed/', methods=['GET', 'POST'], endpoint="rss")
def rss():
    posts = Post.query(Post.status == Post.STATUS_PUBLISHED).order(-Post.modified).fetch(limit=app.config.get("SITE_RSS_NUM"))
    return render_template('rss.xml', posts=posts), 200, {'Content-Type': 'application/rss+xml; charset=utf-8'}


@app.template_filter('md_full')
def md_full_filter(text):
    return markdown.markdown(text, extensions=[
        "markdown.extensions.extra",
        "markdown.extensions.toc",
        "markdown.extensions.nl2br"
    ])


@app.template_filter('md_summary')
def md_summary_filter(text):
    return markdown.markdown(text.split("[========]")[0], extensions=[
        "markdown.extensions.extra",
        "markdown.extensions.nl2br"
    ])
