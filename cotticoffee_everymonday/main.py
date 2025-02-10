# 未成功：blackbox的值未解决，频繁发包会短暂封号

import time
import urllib3
import hashlib
import warnings
import requests
from datetime import date, datetime
from rich.console import Console
from rich.live import Live
from rich.table import Table

console = Console()
warnings.simplefilter("ignore", urllib3.exceptions.InsecureRequestWarning)

setting = {
    "version": "v1",
    "token": "",  # <- 填入账号token
    "Cookie": "",  # <- 填入cookie
    "activityNo": "ttD_0b-FCrPz75AOsCbc26ggj_2oK34PF1F8P2LBg1U",
    "mobile": "",  # <- 填入手机号
    "blackBox": "oWPHF173492237614LTD7nWqb0",
    "appKey": "2YAhmad694MnzqmcPQ5X6TJ6EoSx6sYx",
    "secretKey": "Bu0Zsh4B0SnKBRfds0XWCSn51WJfn5yN",
}


def nowTs():
    timestamp = int(time.time() * 1000)

    return timestamp


def getSign(timestamp):
    text = f"path/cotti-capi/universal/coupon/receiveLaunchRewardH5timestamp{timestamp}version{setting['version']}{setting['secretKey']}"
    sign = hashlib.md5(text.encode("utf-8")).hexdigest().upper()
    print(timestamp)
    print(sign)
    return sign


def whatime():
    try:
        # 根据当前时间戳判断等待或开抢
        today = date.today()
        day = today.day
        mon = today.month
        startime = f"2025-{mon}-{day} 11:00:00.000"
        print("[*] ", startime)
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
                table.add_row("[yellow]剩余时间：", f"{remaining_time} 秒")
                live.update(table)

                time.sleep(0.1)

            live.stop()
    except Exception as e:
        print("[-] Error.....startime\n", e)


def coupon(timestamp, sign):
    url = "https://ma.cotticoffee.com/cotti-capi/universal/coupon/receiveLaunchRewardH5"
    data = {
        "activityNo": setting["activityNo"],
        "mobile": setting["mobile"],
        "comeFrom": "4",
        "openid": None,
        "blackBox": setting["blackBox"],
        "shopMdCode": None,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090b19)XWEB/11159",
        "Content-Type": "application/json",
        "version": setting["version"],
        "split_timestamp": "0",
        "timestamp": str(timestamp),
        "brandMdCode": "20200000006",
        "api-version": "v1",
        "token": setting["token"],
        "sign": sign,
        "appKey": setting["appKey"],
        "Origin": "https://m.cotticoffee.com",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://m.cotticoffee.com/",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": setting["Cookie"],
    }
    print(data)
    response = requests.post(url, json=data, headers=headers, verify=False)
    print(response.text)


def main():
    whatime()
    i = 1
    while i < 8:
        ts = nowTs()
        sign = getSign(ts)
        coupon(ts, sign)
        i += 1
        time.sleep(0.15)


if __name__ == "__main__":
    # main()
    ts = nowTs()
    sign = getSign(ts)
    coupon(ts, sign)
