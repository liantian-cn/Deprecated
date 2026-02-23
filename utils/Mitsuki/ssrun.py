import json
import time
import psutil
import logging
import subprocess

logging.basicConfig(filename='/dev/stdout', level=logging.INFO, format='[WEB] %(asctime)s %(message)s')

server_uuid = None
pid = None


def kill_ss_local():
    if pid is not None:
        try:
            p = psutil.Process(pid)
            p.terminate()
        except:
            pass
    for proc in psutil.process_iter():
        if proc.name() == "ss-local":
            proc.kill()


def is_ss_local_alive():
    for proc in psutil.process_iter():
        if proc.name() == "ss-local":
            if proc.status() != "zombie":
                return True
    return False




def start_ss_local(server):
    cmd = ['/usr/bin/ss-local', '-b', '0.0.0.0', '-l', '1080'] + \
          ['-s', '{}'.format(server["server_addr"])] + \
          ['-p', '{}'.format(server["server_port"])] + \
          ['-k', '{}'.format(server["password"])] + \
          ['-m', '{}'.format(server["method"])] + \
          ['-o', '{}'.format(server["obfs"])] + \
          ['-O', '{}'.format(server["protocol"])] + \
          ['-g', '{}'.format(server["obfsparam"])] + \
          ['-G', '{}'.format(server["protocolparam"])]
    logging.info("Start ss-local use cmd: " + " ".join(cmd))
    return subprocess.Popen(cmd,shell=False,stdin=None,stdout=None,stderr=None,close_fds=True)


if __name__ == '__main__':
    kill_ss_local()
    while True:
        with open('config.json', 'r', encoding='utf-8') as file:
            server = json.loads(file.read())
        if server["uuid"] != server_uuid:
            logging.info("UUID change!")
            kill_ss_local()
            process = start_ss_local(server)
            pid = process.pid
            server_uuid = server["uuid"]

        if not is_ss_local_alive():
            logging.info("SS not Found")
            kill_ss_local()
            start_ss_local(server)
            server_uuid = server["uuid"]
        time.sleep(10)
