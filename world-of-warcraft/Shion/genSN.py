import time
import hashlib


def get_act_code(machine_code):
    return machine_code


if __name__ == "__main__":
    m = input("请输入机器码: ").strip()
    act_code = get_act_code(m)
    print("激活码:", act_code)
    while True:
        time.sleep(10)
