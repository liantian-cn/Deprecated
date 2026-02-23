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

from google.appengine.api import memcache
from google.appengine.api import search
from google.appengine.ext import ndb

from main import app


class Option(ndb.Model):
    raw_value = ndb.TextProperty(verbose_name=u"數值")

    @property
    def value(self):
        return json.loads(self.raw_value, encoding="utf-8")

    @value.setter
    def value(self, value):
        self.raw_value = json.dumps(value, indent=4, encoding="utf-8")


class Category(ndb.Model):
    parent = ndb.KeyProperty(kind="Category", verbose_name=u"父級分類")
    title = ndb.StringProperty(verbose_name=u"内容标题", required=True, indexed=False)
    slug = ndb.StringProperty(verbose_name=u"内容缩略名", required=True)
    description = ndb.TextProperty(verbose_name=u"描述", required=True, indexed=False)
    post_count = ndb.IntegerProperty(indexed=False, default=0, required=True)
    child_count = ndb.IntegerProperty(indexed=False, default=0, required=True)

    @property
    def child(self):
        return Category.query(Category.parent == self.key).fetch()


class Tag(ndb.Model):
    title = ndb.StringProperty(verbose_name=u"内容标题", required=True)


class Archive(ndb.Model):
    time = ndb.DateProperty(required=True)
    post_count = ndb.IntegerProperty(indexed=False)


class Post(ndb.Model):
    STATUS_DRAFT = "draft"
    STATUS_PUBLISHED = "published"
    STATUS_PAGE = "published_page"
    STATUS_DELETED = "deleted"

    STATUS_CHOICES = {STATUS_DRAFT: u"草稿",
                      STATUS_PUBLISHED: u'已發佈(文章)',
                      STATUS_PAGE: u'已發佈(頁面)',
                      STATUS_DELETED: u"已刪除"}
    title = ndb.StringProperty(verbose_name=u"内容标题", required=True, indexed=False)
    slug = ndb.StringProperty(verbose_name=u"内容缩略名")
    created = ndb.DateTimeProperty(verbose_name=u"内容生成时時間", auto_now_add=True)
    modified = ndb.DateTimeProperty(verbose_name=u"内容生成时時間", auto_now=True)
    text = ndb.TextProperty(verbose_name=u"内容文字", required=True, indexed=False)
    category = ndb.KeyProperty(kind=Category, verbose_name=u"分類")
    archive = ndb.KeyProperty(kind=Archive, verbose_name=u"時間")
    tag = ndb.KeyProperty(kind=Tag, repeated=True, verbose_name=u"標簽")
    order = ndb.IntegerProperty(verbose_name=u"排序", default=0)
    status = ndb.StringProperty(verbose_name=u"内容状态", choices=STATUS_CHOICES.keys())

    allowComment = ndb.BooleanProperty(verbose_name=u"是否允许评论", default=True, indexed=False)
    allowPing = ndb.BooleanProperty(verbose_name=u"是否允许ping", default=True, indexed=False)
    allowFeed = ndb.BooleanProperty(verbose_name=u"允许出现在聚合中", default=True, indexed=False)

    @property
    def get_status_display(self):
        return self.STATUS_CHOICES[self.status]

    @property
    def get_category_display(self):
        key = "post_get_category_display_{0}".format(self.category.urlsafe())
        mem = memcache.get(key)
        if mem is None:
            value = self.category.get().title
            memcache.add(key=key, value=value, time=app.config["SITE_MEMCACHED_TIME"])
        else:
            value = mem
        return value

    # @property
    # def get_comment_count(self):
    #     key = "post_get_comment_count_{0}".format(self.key.urlsafe())
    #     mem = memcache.get(key)
    #     if mem is None:
    #         value = Comment.query(Comment.post == self.key).count()
    #         memcache.add(key=key, value=str(value), time=app.config["SITE_MEMCACHED_TIME"])
    #     else:
    #         value = mem
    #     return value

    def _post_put_hook(self, future):

        if self.status == self.STATUS_PUBLISHED:
            doc = search.Document(doc_id=self.key.urlsafe(), fields=[
                search.TextField(name='text', value=self.text),
                search.TextField(name='title', value=self.title),
                search.TextField(name="slug", value=self.slug),
            ])

            search.Index('search-post').put(doc)
        else:
            search.Index('search-post').delete(self.key.urlsafe())

    @classmethod
    def _post_delete_hook(cls, key, future):
        search.Index('search-post').delete(key.urlsafe())


# class Comment(ndb.Model):
#     post = ndb.KeyProperty(kind=Post, verbose_name=u"文章")
#     email = ndb.StringProperty(verbose_name=u"郵件地址", indexed=False)
#     url = ndb.StringProperty(verbose_name=u"網址", indexed=False)
#     nickname = ndb.StringProperty(verbose_name=u"昵稱", required=True, indexed=False)
#     text = ndb.StringProperty(verbose_name=u"内容", required=True, indexed=False)
#     created = ndb.DateTimeProperty(verbose_name=u"内容生成时時間", auto_now_add=True)
