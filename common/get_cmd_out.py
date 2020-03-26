# popen返回文件对象，跟open操作一样
import os

with os.popen(r'git log -1', 'r') as f:
    text = f.read()

commit = str(text).split("\n")[0]
# 打印cmd输出结果