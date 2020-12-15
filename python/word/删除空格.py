# -*- coding=utf-8 -*-
import re

# pip install python-docx
text = """
"""
li = text.split("\n")
i = 0
while i < (len(li) - 1):
    if li[i] == '' and li[i + 1] == '':
        li.__delitem__(i)
    else:
        txt = re.sub(r"([\u4e00-\u9fa5])\s", r'\1', li[i], re.M)
        li[i] = re.sub(r"\s([\u4e00-\u9fa5])", r'\1', txt, re.M)
        i = i + 1

result = ''
for a in li:
    result = result + '\n' + a

print(result)

# txt = re.sub(r"\s{1,3}([\u4e00-\u9fa5])", r'\1', txt, re.M)
# txt = txt.replace("\r\n\r\n", "\r\n")
# txt = txt.replace("\r\n\r\n", "\r\n")
# txt = txt.replace("\r\n\r\n", "\r\n")
# txt = txt.replace("\r\n\r\n", "\r\n")
# txt = txt.replace("\r\n\r\n", "\r\n")
# txt = txt.replace("\r\n\r\n", "\r\n")
# txt = txt.replace("\r\n\r\n", "\r\n")
# print(txt)  # 打印各段落内容文本
