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
from wtforms.validators import Email, URL, DataRequired
from wtforms.widgets.html5 import NumberInput

DEFAULT_OPTION = [
    {
        "option": "SITE_NAME",
        "default_value": "SITE_NAME",
        "label": u"站點名稱",
        "validators": [DataRequired()],
    },
    {
        "option": "SITE_URL",
        "default_value": "http://127.0.0.1:8000",
        "label": u"站點地址",
        "validators": [URL()],
    },
    {
        "option": "SITE_LOGO",
        "default_value": "",
        "label": u"站點LOGO",
        "description": u"若沒有，清留空",
    },
    {
        "option": "SITE_DESCRIPTION",
        "default_value": "SITE_DESCRIPTION",
        "label": u"站點描述",
        "validators": [DataRequired()],
    },
    {
        "option": "SITE_KEY_WORDS",
        "default_value": "site,key,word",
        "label": u"關鍵詞",
        "validators": [DataRequired()],
    },
    {
        "option": "SITE_AUTHOR",
        "default_value": "liantian",
        "label": u"作者名字",
        "validators": [DataRequired()],
    },
    {
        "option": "SITE_EMAIL",
        "default_value": "admininstrator@localhost.local",
        "label": u"作者EMAIL",
        "validators": [DataRequired(), Email()],
    },
    {
        "option": "SITE_LOCALE",
        "default_value": "zh-cn",
        "label": u"編碼",
        "validators": [DataRequired()],
    },
    {
        "option": "SITE_MEMCACHED_TIME",
        "default_value": 3600,
        "label": u"緩存時間",
        "widget": NumberInput(step=360, min=0, max=60 * 60 * 24),
        "description": u"緩存有助於性能提高。",
    },
    {
        "option": "SITE_SIDEBAR_SHOW_RECENT_POST",
        "default_value": True,
        "label": u"側欄：顯示最近文章",
        "description": u"關閉有助於提高性能",
    },
    {
        "option": "SITE_SIDEBAR_RECENT_POST_NUM",
        "default_value": 10,
        "label": u"側欄：文章列表數目",
        "widget": NumberInput(step=1, min=1, max=30),
        "description": u"此數目用於指定顯示在側邊欄中的文章列表數目.",
    },
    # {
    #     "option": "SITE_SIDEBAR_SHOW_RECENT_COMMENT",
    #     "default_value": True,
    #     "label": u"側欄：顯示最近評論",
    #     "description": u"關閉有助於提高性能",
    # },
    # {
    #     "option": "SITE_SIDEBAR_RECENT_COMMENT_NUM",
    #     "default_value": 10,
    #     "label": u"側欄：評論列表數目",
    #     "widget": NumberInput(step=1, min=1, max=20),
    #     "description": u"此數目用於指定顯示在側邊欄中的評論列表數目.",
    # },
    {
        "option": "SITE_SIDEBAR_SHOW_CATEGORY",
        "default_value": True,
        "label": u"側欄：顯示顯示分類",
        "description": u"關閉有助於提高性能",
    },
    {
        "option": "SITE_SIDEBAR_SHOW_ARCHIVE",
        "default_value": True,
        "label": u"側欄：顯示顯示歸檔",
        "description": u"關閉有助於提高性能",
    },
    {
        "option": "SITE_SIDEBAR_ARCHIVE_DATE_FORMAT",
        "default_value": "%B %Y",
        "label": u"側欄：歸檔日期格式",
        "description": u"此格式用於指定顯示在文章歸檔中的日期默認顯示格式，參考http://strftime.org/",
        "validators": [DataRequired()],
    },
    # {
    #     "option": "SITE_COMMENTS_MD",
    #     "default_value": False,
    #     "label": u"評論：使用 Markdown 語法",
    # },
    # {
    #     "option": "SITE_COMMENTS_LINK",
    #     "default_value": True,
    #     "label": u"評論：名稱顯示時自動加上其個人主頁鏈接",
    # },
    # {
    #     "option": "SITE_COMMENTS_NO_FOLLOW",
    #     "default_value": True,
    #     "label": u"評論：對評論者個人主頁鏈接使用 nofollow 屬性",
    # },
    # {
    #     "option": "SITE_COMMENTS_REQUIRED_EMAIL",
    #     "default_value": True,
    #     "label": u"評論：必須填寫郵箱",
    # },
    # {
    #     "option": "SITE_COMMENTS_REQUIRED_LINK",
    #     "default_value": False,
    #     "label": u"評論：必須填寫網址",
    # },
    # {
    #     "option": "SITE_COMMENTS_USE_GRAVATAR",
    #     "default_value": True,
    #     "label": u"評論：啟用 Gravatar 頭像服務",
    # },
    # {
    #     "option": "SITE_COMMENTS_IP_DENY",
    #     "default_value": 60,
    #     "label": u"評論：同一 IP 發布評論的時間間隔限制為,單位是秒",
    #     "widget": NumberInput(step=60, min=60, max=60 * 60 * 24),
    # },
    # {
    #     "option": "SITE_COMMENTS_PER_PAGE",
    #     "default_value": 20,
    #     "label": u"評論：分頁",
    #     "widget": NumberInput(step=1, min=1, max=100),
    #     "description": u"每頁顯示x篇評論, 在列出時將 作為默認顯示",
    # },
    #
    # {
    #     "option": "SITE_COMMENTS_DATETIME_FORMAT",
    #     "default_value": "lll",
    #     "label": u"評論：日期格式",
    #     "description": u"此格式用於指定顯示在評論中的日期默認顯示格式，請參考http://strftime.org/",
    #     "validators": [DataRequired()],
    # },
    {
        "option": "SITE_POST_PER_PAGE",
        "default_value": 10,
        "label": u"文章列表數目",
        "widget": NumberInput(step=1, min=1, max=30),
        "description": u"首頁文章數.",
    },
    {
        "option": "SITE_POST_IMG_WIDTH",
        "default_value": 600,
        "label": u"默認圖片寬度",
        "widget": NumberInput(step=1, min=1, max=2560),
        "description": u"調用Google Image Api處理圖片的寬度。可以在編輯文章時直接修改",
    },
    {
        "option": "SITE_POST_DATETIME_FORMAT",
        "default_value": "%Y-%m-%d",
        "label": u"文章日期格式",
        "description": u"此格式用於指定顯示在文章歸檔中的日期默認顯示格式，請參考http://strftime.org/",
        "validators": [DataRequired()],
    },
    {
        "option": "SITE_ADMIN_POST_PER_PAGE",
        "default_value": 20,
        "label": u"管理員界面文章列表",
        "widget": NumberInput(step=5, min=5, max=50),
        "description": u"此管理員界面文章列表數量",
    },
    {
        "option": "SITE_ALLOWED_EXTENSIONS",
        "default_value": "png,jpg,jpeg,gif,webp,bmp",
        "label": u"允許上傳的文件類型",
        "validators": [DataRequired()],
    },
    {
        "option": "SITE_DISQUS_NAME",
        "default_value": "disqus",
        "label": u"Disqus賬號，訪問disqus.com申請賬號，開啓評論功能",
        "validators": [DataRequired()],
    },
    {
        "option": "SITE_RSS_NUM",
        "default_value": 20,
        "label": u"RSS數量",
        "widget": NumberInput(step=5, min=5, max=50),
    },

]
