import re

from docx import Document as openDoc
from docx.document import Document

document: Document = openDoc(r"C:\Users\bpzj\Desktop\Unix编程艺术\Unix编程艺术.docx")

for paragraph in document.paragraphs:
    if len(paragraph.text) > 1:
        txt = re.sub(r"([\u4e00-\u9fa5])\s", r'\1', paragraph.text, re.M)
        txt = re.sub(r"\s([\u4e00-\u9fa5])", r'\1', txt, re.M)
        txt = txt.replace("曰后", "日后")
        txt = txt.replace("原测", "原则")
        txt = txt.replace("Mcllroy", "McIlroy")
        txt = txt.replace("來", "来")
        txt = txt.replace("縮写", "缩写")
        txt = txt.replace("幵", "开")
        txt = txt.replace("己经", "已经")
        paragraph.text = txt
        print(txt)  # 打印各段落内容文本

document.save(r"C:\Users\bpzj\Desktop\Unix编程艺术\Unix编程艺术.docx")
