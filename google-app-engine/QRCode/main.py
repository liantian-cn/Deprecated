#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'Liantian'
# __email__ = "liantian.me+code@gmail.com"

from io import BytesIO

import qrcode
from flask import Flask, render_template, send_file, request
from qrcode.exceptions import DataOverflowError

ecl_map = {
    'L': qrcode.constants.ERROR_CORRECT_L,
    'M': qrcode.constants.ERROR_CORRECT_H,
    'Q': qrcode.constants.ERROR_CORRECT_Q,
    'H': qrcode.constants.ERROR_CORRECT_H,
}

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return "Error : 404 - Page Not Found", 404


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/api', methods=['GET', 'POST'])
def api():
    data = request.values.get('data', "parameter 'data' is empty\n")

    size = int(request.values.get('size', 4))
    if size < 1 or size > 100 or (not isinstance(size, int)):
        size = 4

    ecl = request.values.get('ecl', "L")
    if ecl not in ['L', 'M', 'Q', 'H']:
        ecl = 'M'
    qr = qrcode.QRCode(error_correction=ecl_map[ecl], box_size=size, border=1)
    qr.add_data(data)

    try:
        qr.make()
    except DataOverflowError:
        return "Error, Data Too Long", 400

    img = qr.make_image()
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
