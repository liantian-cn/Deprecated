#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'Liantian'
# __email__ = "liantian.me+code@gmail.com"
#
# Copyright 2015-2016 liantian
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org>


import io
import mimetypes
import os
import random
import string

from google.appengine.api import images
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.runtime.apiproxy_errors import RequestTooLargeError
from google.appengine.datastore.datastore_query import Cursor

from flask import Flask
from flask import send_file, request, render_template, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFError
from flask_wtf.csrf import CSRFProtect
from mime_map import mime2img_map
from wtforms import TextAreaField, FileField
from wtforms.validators import DataRequired


image_type = ('image/jpeg', 'image/png', 'image/gif')
PER_PAGE = 31

random.seed = (os.urandom(1024))
mimetypes.init()

app = Flask(__name__)
if 'SERVER_SOFTWARE' in os.environ and os.environ['SERVER_SOFTWARE'].startswith('Dev'):
    app.config['DEBUG'] = True

app.secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(32))
app.config['SESSION_KEY'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(32))
app.config['WTF_CSRF_SECRET_KEY'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(32))
app.config['SITE_URL'] = 'https://static.liantian.me'

csrf = CSRFProtect()
csrf.init_app(app)


class Document(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    file = ndb.BlobProperty(compressed=True)
    filename = ndb.StringProperty()
    mime_type = ndb.StringProperty()
    description = ndb.StringProperty()

    def is_image(self):
        return self.mime_type in image_type


class UploadForm(FlaskForm):
    description = TextAreaField('Description:', validators=[DataRequired()])
    file = FileField('File:', validators=[DataRequired()])


@app.route('/', methods=['GET'])
def index():
    curs = Cursor(urlsafe=request.values.get('cursor'))
    form = UploadForm()
    docs, next_cursor, more = Document.query().order(-Document.created).fetch_page(page_size=PER_PAGE,start_cursor=curs,
                                                                                   projection=[Document.filename, Document.description, Document.mime_type]
                                                           )



    return render_template("index.html", form=form, docs=docs,more=more,next_cursor=next_cursor)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.file.data
        filename = f.filename
        mime_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"

        doc = Document()

        doc.filename = filename
        doc.mime_type = mime_type
        doc.description = form.description.data

        if mime_type in image_type:
            f = f.read()
            doc.file = images.im_feeling_lucky(f)
        else:
            doc.file = f.read()
        try:
            doc.put()
        except RequestTooLargeError:
            return "Error : 413 - RequestTooLargeError", 413
    else:
        return render_template("index.html", form=form, docs=[])
    return redirect("/")

@app.route('/delete/<key>', methods=['GET'])
def delete(key):
    ndb.Key(urlsafe=key).delete()
    return redirect("/")


def get_download(key):
    doc = ndb.Key(urlsafe=key).get()
    return send_file(io.BytesIO(doc.file),
                     mimetype=doc.mime_type,
                     as_attachment=True,
                     attachment_filename=doc.filename.encode('utf-8'),
                     add_etags=True,
                     cache_timeout=86400 * 365,
                     conditional=True,
                     last_modified=doc.created)


@app.route('/download/<key>/<filename>', methods=['GET'])
def download(key, filename):
    if request.if_modified_since:
        return "HTTP_304_NOT_MODIFIED", 304
    memcache_key = 'download_{}'.format(key)
    data = memcache.get(memcache_key)
    if data is None:
        data = get_download(key)
        memcache.add(memcache_key, data, 86400 * 30)
    return data


def get_thumbnail(key):
    doc = ndb.Key(urlsafe=key).get()
    thumbnail = images.Image(image_data=doc.file)
    thumbnail.resize(width=200)
    return send_file(io.BytesIO(thumbnail.execute_transforms(output_encoding=images.JPEG, quality=50)),
                     mimetype='image/jpeg',
                     as_attachment=False,
                     attachment_filename="thumbnail_{}".format(doc.filename.encode('utf-8')),
                     add_etags=True,
                     cache_timeout=86400 * 365,
                     conditional=True,
                     last_modified=doc.created)


@app.route('/thumbnail/<key>/<filename>', methods=['GET'])
def thumbnail(key,filename):
    if request.if_modified_since:
        return "HTTP_304_NOT_MODIFIED", 304
    memcache_key = 'thumbnail_{}'.format(key)
    data = memcache.get(memcache_key)
    if data is None:
        data = get_thumbnail(key)
        memcache.add(memcache_key, data, 86400 * 30)
    return data


@app.errorhandler(404)
def page_not_found(e):
    return "Error : 404 - Page Not Found", 404


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return "Error : 403 - CSRFError", 403


@app.template_filter('mime2img')
def mime2img(mime):
    try:
        return url_for('static', filename=mime2img_map[mime])
    except:
        return url_for('static', filename=mime2img_map["application/octet-stream"])
