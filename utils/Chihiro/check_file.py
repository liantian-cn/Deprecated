from config_templates import template, ws_template, tcp_template
from models import VMESSServer, db
import json
import psutil
import time
import logging

logging.basicConfig(filename='/dev/stdout', level=logging.INFO, format='[CHICK_FILE] %(asctime)s %(message)s')

server_uuid = None


def kill_v2ray():
    for proc in psutil.process_iter():
        if proc.name() == "v2ray":
            proc.send_signal(1)


if __name__ == '__main__':

    while True:

        with open('activate', 'r', encoding='utf-8') as file:
            uuid = file.readline().strip()
        if uuid != server_uuid:
            db.connect()
            server = VMESSServer.get(uuid=uuid)

            config = template
            if server.net == "tcp":
                config["outbounds"][0] = tcp_template
            elif server.net == "ws":
                config["outbounds"][0] = ws_template
                config["outbounds"][0]["streamSettings"]["wsSettings"]['path'] = server.path
            config["outbounds"][0]["settings"]["vnext"][0]["address"] = server.add
            config["outbounds"][0]["settings"]["vnext"][0]["port"] = int(server.port)
            config["outbounds"][0]["settings"]["vnext"][0]["users"][0]["alterId"] = int(server.aid)
            config["outbounds"][0]["settings"]["vnext"][0]["users"][0]["id"] = server.id
            config["outbounds"][0]["streamSettings"]["security"] = server.tls
            db.close()
            with open('config.json', 'w', encoding='utf-8') as file:
                file.write(json.dumps(config, indent=4, sort_keys=True))

            logging.info("write new config from  {0} to {1}".format(uuid, server_uuid))
            server_uuid = uuid
            kill_v2ray()
        time.sleep(10)
