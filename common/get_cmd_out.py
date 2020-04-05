# popen返回文件对象，跟open操作一样
import os

with os.popen(r'ipconfig', 'r') as f:
    text = f.read()

print(text)
# 打印cmd输出结果