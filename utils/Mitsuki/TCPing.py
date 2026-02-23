import socket
import time
import sys

__all__ = ["tcp_ping"]


def get_ip(host):
    try:
        remote_ip = socket.gethostbyname(host)
    except:
        print('error: unknown host %s' % host)
        sys.exit(1)
    return remote_ip


def ping(host, port, timeout):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    init_time = time.time()
    try:
        s.connect((host, port))
    except socket.timeout:
        return None
    except Exception as ex:
        # Catches "[Errno 22] Invalid argument" on Linux, e.g., synping 1
        if '22' in str(ex) or 'argument' in str(ex):
            print('error: invalid host %s' % host)
            sys.exit(1)
        # Refused in error means host is alive, otherwise raise the exception
        # like "timed out" so we can catch it on the main loop
        if 'refused' not in str(ex):
            raise (ex)
    end_time = time.time()
    s.close()
    return (end_time - init_time) * 1000


def tcp_ping(host, port=443, timeout=3):
    return ping(get_ip(host), port, timeout)
