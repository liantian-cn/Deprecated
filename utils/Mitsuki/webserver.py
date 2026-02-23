from flask import Flask, render_template,redirect
from models import SSRServer, db
import datetime
import json
import logging
logging.basicConfig(filename='/dev/stdout', level=logging.INFO, format='[WEB] %(asctime)s %(message)s')
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
    except FileNotFoundError :
        activate_uuid = None
    server_list = SSRServer.select().where(SSRServer.active == True).order_by(SSRServer.ep.desc())[:]
    return render_template("index.html", server_list=server_list,activate_uuid=activate_uuid)


@app.route('/activate/<uuid:server_uuid>/')
def activate(server_uuid):
    server = SSRServer.get(uuid=server_uuid)
    write_server(server)
    return redirect("/")


def write_server(server):
    with open('config.json', 'w', encoding='utf-8') as file:
        file.write(
            json.dumps(
                {
                    "uuid": server.uuid,
                    "server_addr": server.server_addr,
                    "server_port": server.server_port,
                    "password": server.password,
                    "method": server.method,
                    "obfs": server.obfs,
                    "protocol": server.protocol,
                    "obfsparam": server.obfsparam,
                    "protocolparam": server.protocolparam,

                }
                , indent=4, sort_keys=True
            )
        )

def read_server():
    with open('config.json', 'r', encoding='utf-8') as file:
        server = json.loads(file.read())
    return server["uuid"]

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
