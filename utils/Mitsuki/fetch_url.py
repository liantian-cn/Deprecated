import requests
import base64
import re
import time
import logging

logging.basicConfig(filename='/dev/stdout', level=logging.INFO, format='[FETCH_URL] %(asctime)s %(message)s')

from models import *


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
        if uri.startswith("ssr://"):
            server = {}
            uri = uri[6:]
            uri = decode_base64(uri)
            splited_uri = re.split(':', uri)
            server['server_addr'] = splited_uri[0]
            server['server_port'] = int(splited_uri[1])
            server['protocol'] = splited_uri[2]
            server['method'] = splited_uri[3]
            server['obfs'] = splited_uri[4]

            pass_param = splited_uri[5]
            pass_param_spilted = re.split('\/\?', pass_param)

            server['password'] = decode_base64(pass_param_spilted[0])

            try:
                obfs_param = re.search('obfsparam=([^&]+)', pass_param_spilted[1]).group(1)
                obfs_param = decode_base64(obfs_param)
            except:
                obfs_param = ""

            server['obfsparam'] = obfs_param

            try:
                protocol_param = re.search(r'protoparam=([^&]+)', pass_param_spilted[1]).group(1)
                protocol_param = decode_base64(protocol_param)
            except:
                protocol_param = ''

            server['protocolparam'] = protocol_param

            try:
                remarks = re.search(r'remarks=([^&]+)', pass_param_spilted[1]).group(1)
                remarks = decode_base64(remarks)
            except:
                remarks = ''

            try:
                group = re.search(r'group=([^&]+)', pass_param_spilted[1]).group(1)
                group = decode_base64(group)
            except:
                group = ''

            server["name"] = "[{0}]{1}".format(group, remarks)
            server_list.append(server)

    return server_list


def init_db(server_list):
    db.create_tables([SSRServer])
    query = SSRServer.update(active=False)
    query.execute()
    for server in server_list:
        ssrserver, created = SSRServer.get_or_create(
            server_addr=server["server_addr"],
            server_port=server["server_port"])
        ssrserver.protocol = server["protocol"]
        ssrserver.method = server["method"]
        ssrserver.obfs = server["obfs"]
        ssrserver.password = server["password"]
        ssrserver.obfsparam = server["obfsparam"]
        ssrserver.protocolparam = server["protocolparam"]
        ssrserver.name = server["name"]
        ssrserver.active = True
        ssrserver.save()
        if created:
            logging.info("Created: {0}:{1}".format(server["server_addr"],server["server_port"]))
        else:
            logging.info("Update: {0}:{1}".format(server["server_addr"], server["server_port"]))

if __name__ == '__main__':
    # init_db(server_list=url_to_list(url=sys.argv[1]))
    with open("subscribe","r",encoding='utf-8') as file:
        url = file.readline()

    while True:
        init_db(server_list=url_to_list(url))
        time.sleep(1800)