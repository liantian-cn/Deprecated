import base64
import json
import time
import logging
import requests

from models import *

logging.basicConfig(filename='/dev/stdout', level=logging.INFO, format='[FETCH_URL] %(asctime)s %(message)s')


def decode_base64(data):
    missing_padding = len(data) % 4
    if missing_padding != 0:
        if isinstance(data, bytes):
            data += b'=' * (4 - missing_padding)
        if isinstance(data, str):
            data += '=' * (4 - missing_padding)
    return base64.urlsafe_b64decode(data).decode("utf-8")


def url_to_list(url):
    response = requests.get(url)
    server_list = []
    for uri in [line.strip() for line in decode_base64(response.content).split()]:
        if uri.startswith("vmess://"):
            uri = uri[8:]
            uri = decode_base64(uri)
            server = json.loads(uri)
            server_list.append(server)
    return server_list


def init_db(server_list):
    db.create_tables([VMESSServer])
    VMESSServer.update(active=False).execute()
    for d in server_list:
        _, created = VMESSServer.get_or_create(add=d["add"], port=d["port"])
        VMESSServer.update(active=True, **d).where(VMESSServer.add == d["add"], VMESSServer.port == d["port"]).execute()

        if created:
            logging.info("Created: {0}:{1}".format(d["add"], d["port"]))
        else:
            logging.info("Update: {0}:{1}".format(d["add"], d["port"]))


if __name__ == '__main__':
    # init_db(server_list=url_to_list(url=sys.argv[1]))
    with open("subscribe", "r", encoding='utf-8') as file:
        url = file.readline()

    while True:
        init_db(server_list=url_to_list(url))
        time.sleep(1800)
