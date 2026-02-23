#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time

import pytz
import pathlib

from miio import CloudInterface
from miio import Yeelight
from miio.exceptions import DeviceException

from astral import LocationInfo
from astral.sun import sun
from datetime import datetime, timedelta

config_file_path = pathlib.Path(__file__).parent.joinpath("config.json")

config = json.load(open(config_file_path))

__doc__ = """


pip install python-miio
pip install astral
pip install pytz  

"""


def calculate_sunrise_sunset():
    # 定位信息
    location = LocationInfo(latitude=config["latitude"], longitude=config["longitude"], timezone=config["timezone"])

    # 获取今天的日期
    today = datetime.today()

    # 计算日出和日落时间
    s = sun(location.observer, date=today, tzinfo=location.timezone)
    # print(s)

    # 返回日出和日落时间
    return s['sunrise'], s['noon'], s['sunset']


def get_light_properties(model='yeelink.light.ceil32'):
    utc_now = datetime.now(pytz.UTC)
    now = utc_now.astimezone(pytz.timezone(config["timezone"]))
    sunrise, noon, sunset = calculate_sunrise_sunset()

    before_sunrise = now < sunrise - timedelta(hours=1)
    after_sunset = now > sunset + timedelta(hours=1)
    is_noon = now == noon
    brightness = min_brightness = config["min_brightness"]
    max_brightness = config["max_brightness"]
    temperature = min_temperature = config["min_temperature"]
    max_temperature = config["max_temperature"]
    # 根据时间关系设置色温和亮度

    if model == "yeelink.light.ceil38":
        min_brightness = max(40, min_brightness)

    if before_sunrise or after_sunset:
        print("日出前1小时和日落后1小时，设置最低亮度和色温")

        brightness = min_brightness
        temperature = min_temperature
    elif is_noon:
        # 正午时间，设置最大亮度和最低色温
        brightness = max_brightness
        temperature = max_temperature
    elif now < noon:
        print("计算上午的时间比例")
        time_since_sunrise = (now - sunrise).total_seconds()
        time_until_noon = (noon - sunrise).total_seconds()

        # 计算亮度
        brightness = min_brightness + (max_brightness - min_brightness) * (time_since_sunrise / time_until_noon)

        # 计算色温
        temperature = min_temperature + (max_temperature - min_temperature) * (time_since_sunrise / time_until_noon)
    elif now > noon:
        print("计算下午的时间比例")
        time_since_noon = (now - noon).total_seconds()
        time_until_sunset = (sunset - noon).total_seconds()

        # 计算亮度
        brightness = max_brightness - (max_brightness - min_brightness) * (time_until_sunset/time_since_noon )

        # 计算色温
        temperature = max_temperature - (max_temperature - min_temperature) * (time_until_sunset/time_since_noon )
    return int(brightness), int(temperature)


def main():
    if len(config["devices"]) == 0:
        devices = []
        print("当前没有设备，请输入设备登录信息，录入设备\n")
        username = input("请输入米家账号：")
        password = input("请输入米家密码：")
        ci = CloudInterface(username=username, password=password)
        devs = ci.get_devices()
        for did, dev in devs.items():
            print(dev)
            if dev.model.startswith("yeelink"):
                devices.append({
                    "model": dev.model,
                    "token": dev.token,
                    "ip": dev.ip,
                    "name": dev.name
                })
        config["devices"] = devices

        json.dump(config, open(config_file_path, "w", encoding="utf-8"), indent=4)
    else:
        while True:
            for dev in config["devices"]:
                print("=======================")
                brightness, temperature = get_light_properties(dev["model"])
                print(f'{dev["name"]} set to brightness -> {brightness}  temperature-> {temperature}')
                if dev["model"].startswith("yeelink"):
                    try:
                        d = Yeelight(dev["ip"], dev["token"])
                        d.set_save_state_on_change(True)
                        d.set_brightness(brightness)
                        # d.set_color_temp(temperature)

                    except DeviceException as e:
                        print(f'更新{dev["name"]}故障')
                        print(e)
                time.sleep(300)


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    main()
