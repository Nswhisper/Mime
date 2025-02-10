# -*- coding=utf-8 -*-
import time
import random
import sys, os
import logging
import requests
import warnings
import urllib3
from datetime import date
from rich.live import Live
from rich.table import Table
from datetime import datetime
from rich.console import Console
from logging.handlers import TimedRotatingFileHandler
warnings.simplefilter("ignore", urllib3.exceptions.InsecureRequestWarning)

session = requests.session()
console = Console()
selected = {}

#  /citiccard/lottery-gateway-pay/act-info.do?actId=KFKZZLHD  # 抓取该请求的cookie值

with open("cookie.txt", "r", encoding="utf-8") as f:
    cookie = f.read().strip()


def random_delay(i):
    delay_time = random.uniform(0, i)
    time.sleep(delay_time)


def a_request(url, method, params="", data=""):
    url = "https://ldp.creditcard.ecitic.com/" + url
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 DKKJ/11.3.1/[DKKJ_TOWER_1.2] DKKJ_V4 dkkj_channel_id/AppStore/UnionPay/1.0 DKKJ/Theme/DKKJ-NORMAL",
        "x-requested-with": "XMLHttpRequest",
        "Sec-Fetch-Site": "same-origin",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Sec-Fetch-Mode": "cors",
        "Content-Type": "application/json; charset=utf-8",
        "deviceInfo": "undefined",
        "Referer": "https://ldp.creditcard.ecitic.com/citiccard/lotteryfrontend/CoffeeCard.html",
        "Sec-Fetch-Dest": "empty",
        "Cookie": cookie,
    }
    if method == "get":
        r = session.get(
            url,
            headers=headers,
            params=params,
            timeout=0.5,
            verify=False,
        )
        if r.ok and "resultData" in r.text:
            res_data = r.json()["resultData"]
        else:
            res_data = r.text
            logging.info(res_data)

    elif method == "post":
        r = session.post(
            url, headers=headers, json=data, timeout=0.5, verify=False
        )
        logging.info(r.text)
        if r.ok and "retMsg" in r.text:
            res_data = r.json()["retMsg"]
        else:
            res_data = r.json()
            logging.info(res_data)

    return res_data


def gen_logs():
    current_file_path = os.path.abspath(__file__)
    log_file_path = os.path.join(current_file_path, "../runtime.log")
    handler = TimedRotatingFileHandler(
        log_file_path, when="midnight", interval=1, backupCount=7
    )

    logging.basicConfig(
        handlers=[handler],
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


# 毫秒级倒计时
def ontime():
    today = date.today()
    mon = today.month
    day = today.day
    startime = f"2025-{mon}-{day} 10:00:00.000"
    time_format = "%Y-%m-%d %H:%M:%S.%f"
    startime = int(datetime.strptime(startime, time_format).timestamp() * 1000)
    current_timestamp = int(time.time() * 1000)
    with Live(console=console, refresh_per_second=10) as live:
        while current_timestamp < startime:
            current_timestamp = int(time.time() * 1000)
            remaining_time = float(startime - current_timestamp) / 1000.0
            if remaining_time < 0.1:
                break
            table = Table(title="", show_header=False, box=None)
            table.add_row("[yellow]倒计时：", f"{remaining_time} 秒")
            live.update(table)

            time.sleep(0.1)

        live.stop()


def get_Id():
    url = "citiccard/lottery-gateway-pay/prizes.do"
    params = {"actId": "KFKZZLHD"}
    response = a_request(url, "get", params)
    for index, goodsinfo in enumerate(response):
        #  9元瑞幸咖啡立减金    9元微信立减金
        if goodsinfo["goodsName"] == "9元瑞幸咖啡立减金":
            selected["goodsId"] = goodsinfo["goodsId"]
    logging.info(selected)


def format_msts(timestamp):
    timestamp_seconds = timestamp / 1000
    dt = datetime.fromtimestamp(timestamp_seconds)
    formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    print("[*] 执行时间记录 ", formatted_time)
    logging.info("执行时间记录 " + str(formatted_time))


def submit():
    try:
        url = (
            "citiccard/lottery-gateway-pay/mkt-service/lottery-and-obtain-mkt-addr-info"
        )
        data = {"actId": "KFKZZLHD", "rewardGroupId": selected["goodsId"]}
        i = 1
        while i < 6:
            response = a_request(url, "post", data)
            if response == "成功":
                format_msts(int(time.time() * 1000))
                print("[+] success")
                break
            elif response == "今日礼品已领完，请明天再来哟":
                print("[-]", response)
                format_msts(int(time.time() * 1000))
                i += 2
                continue
            elif response["result"] == "time out":
                print("[-] Cookie超时")
                format_msts(int(time.time() * 1000))
                break
            else:
                print(response)
                format_msts(int(time.time() * 1000))
                i += 1
                random_delay(0.1)

    except Exception as e:
        logging.error(e)


def main():
    gen_logs()
    get_Id()
    ontime()
    submit()


if __name__ == "__main__":
    main()
