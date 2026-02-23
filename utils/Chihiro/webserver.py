from flask import Flask, render_template, redirect
from models import *
import datetime


db.connect()

app = Flask(__name__, static_url_path='/static')


@app.template_filter()
def time_ago(value):
    now = datetime.datetime.now()
    d = now - value
    return "{0}s ago".format(d.seconds)


@app.route('/')
def index():
    try:
        activate_uuid = read_server()
    except FileNotFoundError:
        activate_uuid = None
    server_list = VMESSServer.select().where(VMESSServer.active == True).order_by(VMESSServer.ep.desc())[:]
    return render_template("index.html", server_list=server_list, activate_uuid=activate_uuid)


@app.route('/activate/<uuid:server_uuid>/')
def activate(server_uuid):
    server = VMESSServer.get(uuid=server_uuid)
    write_server(server.uuid)
    return redirect("/")


def write_server(uuid):
    with open('activate', 'w', encoding='utf-8') as file:
        file.write(uuid)


def read_server():
    with open('activate', 'r', encoding='utf-8') as file:
        uuid = file.readline().strip()
    return uuid


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
