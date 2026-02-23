import datetime
import random
import time
import logging
from models import *
from tcping import tcping

logging.basicConfig(filename='/dev/stdout', level=logging.INFO, format='[MONITOR] %(asctime)s %(message)s')

INTERVAL = 600
ATTENUATION = 0.96


def score(ping_latency=None):
    if ping_latency is None:
        return float(0)
    elif ping_latency > 600:
        return float(4)
    elif ping_latency > 500:
        return float(5)
    elif ping_latency > 400:
        return float(6)
    elif ping_latency > 350:
        return float(7)
    elif ping_latency > 300:
        return float(8)
    elif ping_latency > 250:
        return float(9)
    elif ping_latency > 200:
        return float(10)
    elif ping_latency > 180:
        return float(11)
    elif ping_latency > 160:
        return float(12)
    elif ping_latency > 140:
        return float(13)
    elif ping_latency > 120:
        return float(14)
    elif ping_latency > 100:
        return float(15)
    elif ping_latency > 90:
        return float(16)
    elif ping_latency > 80:
        return float(17)
    elif ping_latency > 70:
        return float(18)
    elif ping_latency > 60:
        return float(19)
    else:
        return float(20)


def test_update_server(add, port, uuid, old_ep):
    result = tcping(add, int(port))
    new_ep = old_ep * ATTENUATION + score(result)

    VMESSServer.update(
        latest_tests=datetime.datetime.now(),
        test_result=result or "timeout",
        ep=new_ep
    ).where(VMESSServer.uuid == uuid).execute()

    logging.info("{uuid}:{result}".format(uuid=uuid, result=result))

    return result or 3000


def test_all_server():
    start = time.time()
    server_need_to_test = VMESSServer.select().where(VMESSServer.active == True).order_by(
        VMESSServer.latest_tests.asc())[:]
    random.shuffle(server_need_to_test)
    for server in server_need_to_test:
        test_update_server(server.add, server.port, server.uuid, server.ep)
        time.sleep(random.choice(range(2000, 5000)) / 1000)
    return time.time() - start


if __name__ == '__main__':
    db.connect()
    while True:
        tt = test_all_server()
        v = INTERVAL - tt
        if v < 0: v = 0
        logging.info("Sleep {}".format(v / 1000))
        time.sleep(v / 1000)
