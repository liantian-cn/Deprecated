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

import os
import pprint
import io
import json
import urllib
from datetime import datetime
from netaddr import IPNetwork, AddrFormatError, cidr_merge

from flask import Flask, request, render_template, redirect, send_file, make_response, jsonify

app = Flask(__name__)
if 'SERVER_SOFTWARE' in os.environ and os.environ['SERVER_SOFTWARE'].startswith('Dev'):
    app.debug = True
else:
    app.debug = False


def format_network(network, fmt):
    fmt = fmt.strip().lower()
    if fmt == "acl" or fmt == u"acl":
        return "{0}/{1}".format(network.network, network.hostmask)
    elif fmt == "netmask" or fmt == u"netmask":
        return "{0}/{1}".format(network.network, network.netmask)
    else:
        return str(network)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/api', methods=['POST'])
def api():
    ip_list = request.values.get('ip_list', None)
    return_json = request.values.get('json', False)
    fmt = request.values.get('format', "cidr")
    fmt = fmt.encode("utf-8")
    su = request.values.get('super', "32")
    su = int(su.encode("utf-8"))

    if ip_list:
        ip_list = ip_list
        line_num = 0
        groups = dict()
        errors = []
        for line in ip_list.splitlines():
            line_num += 1
            original_line = line.strip()
            line = line.strip()

            if line.startswith("#") or line.startswith(u"#"):
                continue

            if line == "":
                continue

            line = line.split("#", 1)[0].strip()

            g = line.split(None, 1)
            if len(g) > 1:
                groupname = g[1].strip()
            else:
                groupname = "root"
            ips = g[0].strip()
            try:
                nw = IPNetwork(ips)
                if nw.prefixlen > su:
                    nw = nw.supernet(su)[0]
            except AddrFormatError:
                errors.append({
                    "line_num": line_num,
                    "original_line": original_line,
                    "display": "Line No.{0:<8}:{1}".format(line_num, original_line)
                })
                continue
            group = groups.get(groupname, [])
            group.append(nw)
            groups[groupname] = group

        summarized_networks = []
        for key, value in groups.iteritems():
            summarized_networks.append({
                "group_name": key,
                "summarized_networks": [format_network(x, fmt) for x in cidr_merge(value)]
            })
    if bool(return_json):
        response = make_response(jsonify(errors=errors, summarized_networks=summarized_networks))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
        return response
    return render_template("result.html", errors=errors, summarized_networks=summarized_networks)
