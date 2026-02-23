#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'Liantian'
# __email__ = "liantian.me+code@gmail.com"

import base64
import binascii
from io import BytesIO

from PIL import Image
from flask import Flask, render_template, redirect, send_file
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired


class MergeForm(FlaskForm):
    file = FileField(validators=[DataRequired()])
    img = FileField(validators=[DataRequired()])
    submit = SubmitField()


class SplitForm(FlaskForm):
    img = FileField(validators=[DataRequired()])
    submit = SubmitField()


app = Flask(__name__)
CSRFProtect(app)
app.config["SECRET_KEY"] = "https://hidefile.liantian.me/"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def split_bin(s):
    return [s[i * 4:i * 4 + 4] for i in range(0, int(len(s) / 4))]


def mod_pix(pix, data):
    result = []
    for i in range(0, 4):
        if pix[i] % 2 == int(data[i]):
            result.append(pix[i])
        elif pix[i] < 127:
            result.append(pix[i] + 1)
        else:
            result.append(pix[i] - 1)
    return tuple(result)


def read_pix(pix):
    result = []
    for i in range(0, 4):
        result.append(str(pix[i] % 2))

    return "".join(result)


@app.errorhandler(404)
def page_not_found(e):
    return "Error : 404 - Page Not Found", 404


@app.route('/', methods=['GET'])
def index():
    m_form = MergeForm()
    s_form = SplitForm()
    return render_template("index.html", m_form=m_form, s_form=s_form)


@app.route('/merge', methods=["POST"])
def merge():
    m_form = MergeForm()
    if m_form.validate_on_submit():

        try:
            im = Image.open(m_form.img.data)
        except:
            return "Not img file"
        file_b = m_form.file.data.read()
        if len(file_b) > 2 * 1024 * 1024:
            return "too big file"
        c = bin(int((base64.b64encode(file_b) + b"__").hex(), base=16))[2:]
        d = (8 - (len(c) % 8)) * "0" + c
        if len(d) > im.size[0] * im.size[1] * 8:
            return "smaller file, bigger img."
        e = split_bin(d)
        img = im.convert('RGBA')
        pixels = img.load()
        count = 0
        for i in range(img.size[0]):  # for every pixel:
            for j in range(img.size[1]):
                if count == len(e):
                    break
                pixels[i, j] = mod_pix(pixels[i, j], e[count])
                count += 1
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png', as_attachment=True, attachment_filename="merge.png")
    return redirect("/")


@app.route('/split', methods=["POST"])
def split():
    s_form = SplitForm()
    if s_form.validate_on_submit():
        try:
            img = Image.open(s_form.img.data)
        except:
            return "Not img file"
        pixels = img.load()
        result = []
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                result.append(read_pix(pixels[i, j]))
        buffer = BytesIO()
        buffer.write(base64.b64decode(binascii.a2b_hex(hex(int("".join(result), 2))[2:]).split(b"__")[0]))
        buffer.seek(0)
        return send_file(buffer, mimetype='application/octet-stream', as_attachment=True,
                         attachment_filename="splitfile")
    return redirect("/")


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
