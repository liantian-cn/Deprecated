import datetime
import random
import time
import logging

logging.basicConfig(filename='/dev/stdout', level=logging.INFO, format='[MONITOR] %(asctime)s %(message)s')
INTERVAL = 600
ATTENUATION = 0.9

from models import *
from TCPing import tcp_ping


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


def test_update_server(server):
    result = tcp_ping(server.server_addr, server.server_port)
    old_ep = server.ep
    new_ep = old_ep * ATTENUATION + score(result)
    server.latest_tests = datetime.datetime.now()
    server.test_result = result or "timeout"
    server.ep = new_ep
    logging.info("{server_addr}:{server_port} EP:{ep:.2f}  RESULT: {result}".format(server_addr=server.server_addr,
                                                                                    server_port=server.server_port,
                                                                                    result=result,
                                                                                    ep=new_ep))
    server.save()
    return result or 3000


def test_all_server():
    active_count = SSRServer.select().where(SSRServer.active == True).count()
    time_stamp = sorted(random.sample(list(range(0, int(INTERVAL/2))), active_count))
    spacer = [time_stamp[i] - time_stamp[i - 1] for i in range(1, len(time_stamp))] + 100 * [5]
    server_need_to_test = SSRServer.select().where(SSRServer.active == True).order_by(SSRServer.latest_tests.asc())[:]
    random.shuffle(server_need_to_test)
    t = 0
    total_time = float(0)
    for server in server_need_to_test:
        use_time = test_update_server(server)
        time.sleep(spacer[t])
        t += 1
        total_time = total_time + spacer[t] * 1000 + use_time
    return total_time


if __name__ == '__main__':
    db.connect()
    while True:
        tt = test_all_server()
        v = INTERVAL * 1000 - tt
        if v < 0: v = 0
        logging.info("Sleep {}".format(v/1000))
        time.sleep(v / 1000)
