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

from datetime import datetime, date

from flask import request
from flask_wtf.form import FlaskForm
from google.appengine.ext import ndb
from slugify import slugify
from wtforms.fields import StringField, SelectField, TextAreaField, BooleanField, SubmitField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import DataRequired, Regexp
from wtforms.widgets import TextInput, CheckboxInput
from wtforms.widgets.html5 import NumberInput

from default_option import DEFAULT_OPTION
from main import app
from models import Option, Post, Tag, Category, Archive
from utils import pretty_slug


class SiteOptionForm(FlaskForm, object):

    def __init__(self, *args, **kwargs):
        for opt in DEFAULT_OPTION:
            if isinstance(opt["default_value"], bool):
                name = opt["option"]
                field = BooleanField(
                    label=opt["label"],
                    default=app.config.get(name, opt["default_value"]),
                    description=opt.get("description", ""),
                    widget=opt.get("widget", CheckboxInput())
                )
            elif isinstance(opt["default_value"], str):
                name = opt["option"]
                field = StringField(
                    label=opt["label"],
                    default=app.config.get(name, opt["default_value"]),
                    validators=opt.get("validators", []),
                    description=opt.get("description", ""),
                    widget=opt.get("widget", TextInput())
                )

            elif isinstance(opt["default_value"], int):
                name = opt["option"]
                field = IntegerField(
                    label=opt["label"],
                    default=opt["default_value"],
                    validators=opt.get("validators", []),
                    description=opt.get("description", ""),
                    widget=opt.get("widget", NumberInput(step='1'))
                )
            setattr(self, name, field)
            self._unbound_fields = self._unbound_fields + [[name, field]]
        setattr(self, "submit", SubmitField(label=u"提交"))
        self._unbound_fields = self._unbound_fields + [["submit", SubmitField(label=u"提交")]]

        super(SiteOptionForm, self).__init__(*args, **kwargs)

    def save(self):
        for field_name, value in self._fields.iteritems():
            if field_name.upper().startswith("SITE_"):
                value = self._fields[field_name].data
                app.config[field_name] = value
                op = Option(id=field_name)
                op.value = value
                op.put()


#
# class OLDSiteOptionForm(FlaskForm, object):
#     SITE_NAME = StringField(label=u"站點名稱", validators=[DataRequired()], default=app.config.get("SITE_NAME", ""))
#     SITE_URL = URLField(label=u"站點地址", validators=[DataRequired()], default=app.config.get("SITE_URL", ""))
#     SITE_DESCRIPTION = StringField(label=u"站點描述", validators=[DataRequired()], default=app.config.get("SITE_DESCRIPTION", ""))
#     SITE_KEY_WORDS = StringField(label=u"關鍵詞", validators=[DataRequired()], default=app.config.get("SITE_KEY_WORDS", ""))
#     SITE_AUTHOR = StringField(label=u"作者名字", validators=[DataRequired()], default=app.config.get("SITE_AUTHOR", ""))
#     SITE_EMAIL = EmailField(label=u"作者EMAIL", validators=[DataRequired(), Email()], default=app.config.get("SITE_EMAIL", ""))
#     SITE_LOCALE = StringField(label=u"編碼", validators=[DataRequired()], default=app.config.get("SITE_LOCALE", "zh-cn"))
#     SITE_MEMCACHED_TIME = IntegerField(label=u"緩存時間", description=u"緩存有助於性能提高。", default=app.config.get("SITE_MEMCACHED_TIME", 3600), widget=NumberInput(step=360, min=0, max=60 * 60 * 24))
#
#     SITE_COMMENTS_MD = BooleanField(label=u"在評論中使用 Markdown 語法", default=app.config.get("SITE_COMMENTS_MD", False))
#     SITE_COMMENTS_LINK = BooleanField(label=u"評論者名稱顯示時自動加上其個人主頁鏈接", default=app.config.get("SITE_COMMENTS_LINK", True))
#     SITE_COMMENTS_NO_FOLLOW = BooleanField(label=u"對評論者個人主頁鏈接使用 nofollow 屬性", default=app.config.get("SITE_COMMENTS_NO_FOLLOW", True))
#     SITE_COMMENTS_REQUIRED_EMAIL = BooleanField(label=u"對評必須填寫郵箱", default=app.config.get("SITE_COMMENTS_REQUIRED_EMAIL", True))
#     SITE_COMMENTS_REQUIRED_LINK = BooleanField(label=u"對評必須填寫網址", default=app.config.get("SITE_COMMENTS_REQUIRED_LINK", False))
#     SITE_COMMENTS_USE_GRAVATAR = BooleanField(label=u"評論啟用 Gravatar 頭像服務", default=app.config.get("SITE_COMMENTS_USE_GRAVATAR", True))
#     SITE_COMMENTS_IP_DENY = IntegerField(label=u"同一 IP 發布評論的時間間隔限制為,單位是秒", default=app.config.get("SITE_COMMENTS_IP_DENY", 60), widget=NumberInput(step=60, min=60, max=60 * 60 * 24))
#     SITE_COMMENTS_PER_PAGE = IntegerField(label=u"評論分頁", description=u"每頁顯示x篇評論, 在列出時將 作為默認顯示", default=app.config.get("SITE_COMMENTS_PER_PAGE", 20), widget=NumberInput(step=1, min=1, max=100))
#     SITE_COMMENTS_LIST_NUM = IntegerField(label=u"評論列表數目", description=u"此數目用於指定顯示在側邊欄中的評論列表數目.", default=app.config.get("SITE_COMMENTS_LIST_NUM", 10), widget=NumberInput(step=1, min=1, max=20))
#     SITE_COMMENTS_DATETIME_FORMAT = StringField(label=u"評論日期格式", description=u"此格式用於指定顯示在評論中的日期默認顯示格式，請參考momentjs.com", default=app.config.get("SITE_COMMENTS_DATETIME_FORMAT", "lll"))
#
#     SITE_POST_LIST_NUM = IntegerField(label=u"文章列表數目", description=u"此數目用於指定顯示在側邊欄中的文章列表數目.", default=app.config.get("SITE_POST_LIST_NUM", 10), widget=NumberInput(step=1, min=1, max=30))
#     SITE_POST_PER_PAGE = IntegerField(label=u"每頁文章數目", description=u"此數目用於指定文章歸檔輸出時每頁顯示的文章數目.", default=app.config.get("SITE_POST_PER_PAGE", 5), widget=NumberInput(step=1, min=1, max=30))
#     SITE_POST_DATETIME_FORMAT = StringField(label=u"文章日期格式", description=u"此格式用於指定顯示在文章歸檔中的日期默認顯示格式，請參考momentjs.com", default=app.config.get("SITE_POST_DATETIME_FORMAT", "L"))
#
#     SITE_ADMIN_POST_PER_PAGE = IntegerField(label=u"管理員界面文章列表", description=u"管理員界面文章列表數量", default=app.config.get("SITE_ADMIN_POST_PER_PAGE", 20), widget=NumberInput(step=5, min=5, max=50))
#     SITE_ALLOWED_EXTENSIONS = StringField(label=u"允許上傳的文件類型", description=u"使用英文的,分離", default=app.config.get("SITE_ALLOWED_EXTENSIONS", "txt,pdf,png,jpg,jpeg,gif,webp,bmp"))
#
#     submit = SubmitField(label=u"提交")
#
#     def save(self):
#         for field_name, value in self._fields.iteritems():
#             if field_name.upper().startswith("SITE_"):
#                 value = self._fields[field_name].data
#                 app.config[field_name] = value
#                 op = Option(id=field_name)
#                 op.value = value
#                 op.put()


class PostForm(FlaskForm, object):
    title = StringField(label=u"标题", validators=[DataRequired()])
    slug = StringField(label=u"缩略名", validators=[Regexp("^[-\w]*$")], description=u"僅可使用英文、數字、下劃綫。每個文章應該有不同的縮略。如果留空，將自動生成")
    text = TextAreaField(label=u"内容文字", validators=[DataRequired()], description=u"使用兼容于Github的Markdown語法。")
    category = SelectField(label=u"分類", choices=[("", "")], default="")
    tag = StringField(label=u"標簽", description=u"使用英文半角逗號\" , \"分隔。同樣英文google翻譯的tag會被覆蓋。")
    order = IntegerField(label=u"排序", description=u"默認值為0，大於0可實現置頂效果。", widget=NumberInput(step=1, min=0, max=10), default=0)
    allowComment = BooleanField(label=u"是否允许评论", default=True)
    allowPing = BooleanField(label=u"是否允许ping", default=True)
    allowFeed = BooleanField(label=u"允许出现在聚合中", default=True)
    status = SelectField(label=u"内容状态", choices=[(k, v) for k, v in Post.STATUS_CHOICES.iteritems()], default=Post.STATUS_DRAFT)

    def __init__(self, obj=None, **kwargs):
        super(PostForm, self).__init__(obj=obj, **kwargs)
        self.category.choices = [("", "--------------------------")] + [(c.key.urlsafe(), c.title) for c in Category.query().fetch()]
        self.obj = obj
        if (obj is not None) and ((not bool(request)) or request.method in ['GET']):
            self.tag.data = " , ".join([t.get().title for t in obj.tag])
            if obj.category is not None:
                self.category.data = obj.category.urlsafe()
            else:
                self.category.data = ""

    def save(self):
        if self.obj is None:
            post = Post()
        else:
            post = self.obj

        # make slug
        title = self.title.data
        if (self.slug.data is None) or (self.slug.data.strip() == "") or (self.slug.data.strip() == u""):
            slug = pretty_slug(title)
        else:
            slug = slugify(self.slug.data.strip())

        # category
        if (self.category.data.strip() is "") or (self.category.data.strip() is u""):
            category = None
        else:
            category = ndb.Key(urlsafe=self.category.data.strip())

        # tag
        tag = []
        for word in self.tag.data.split(","):
            word = word.strip()
            if not word == "":
                t = Tag(id=pretty_slug(word).lower())
                t.title = word
                key = t.put()
                tag.append(key)

        t = datetime.now()
        archive = Archive(id=t.strftime("%Y_%m"))
        archive.time = date(year=t.year, month=t.month, day=1)
        archive_key = archive.put()

        post.title = title
        post.slug = slug
        post.text = self.text.data

        post.category = category
        post.tag = tag
        post.archive = archive_key

        post.order = self.order.data
        post.status = self.status.data
        post.allowComment = self.allowComment.data
        post.allowPing = self.allowPing.data
        post.allowFeed = self.allowFeed.data

        post.put()
        app.config["LATEST"] = datetime.now()


class NewPostForm(PostForm):
    submit = SubmitField(label=u"新建")


class EditPostForm(PostForm):
    submit = SubmitField(label=u"修改")


class NewCategoryForm(FlaskForm, object):
    title = StringField(label=u"标题", validators=[DataRequired()])
    # slug = StringField(label=u"缩略名", validators=[Regexp("^[-\w]*$")], description=u"僅可使用英文、數字、下劃綫。每個文章應該有不同的縮略。如果留空，將自動生成")
    parent = SelectField(label=u"父級分類", choices=[("", "")], default="")
    description = TextAreaField(label=u"描述")
    submit = SubmitField(label=u"新建")

    def __init__(self, **kwargs):
        super(NewCategoryForm, self).__init__(**kwargs)
        self.parent.choices = [("", "--------------------------")] + [(c.key.urlsafe(), c.title) for c in Category.query(Category.parent == None).fetch()]

    def save(self):
        category = Category()
        category.title = self.title.data.strip()
        category.slug = pretty_slug(self.title.data).strip()
        category.description = self.description.data
        if (self.parent.data.strip() is "") or (self.parent.data.strip() is u""):
            category.parent = None
        else:
            category.parent = ndb.Key(urlsafe=self.parent.data.strip())
        category.put()
