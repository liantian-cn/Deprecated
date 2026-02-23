#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'Liantian'
# __email__ = "liantian.me+code@gmail.com"

import os
import random

from flask import Flask, request, jsonify,redirect

app = Flask(__name__)

random.seed = (os.urandom(1024))


@app.errorhandler(404)
def page_not_found(e):
    return redirect("/api")


@app.route('/api', methods=['GET', 'POST'])
def genpass():
    try:
        length = int(request.values.get('length', 32))
    except:
        length = 32

    chars = str(request.values.get('chars', '2346789BCDFGHJKMPQRTVWXY'))

    return jsonify(
        length=length,
        chars=chars,
        result=''.join(random.choice(chars) for i in range(length))
    )


if __name__ == '__main__':
    app.run()
