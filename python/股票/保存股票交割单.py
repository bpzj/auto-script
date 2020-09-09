import datetime
from typing import List

import win32clipboard as w
import win32con
import xlwings
from xlwings import Sheet

"""用于保存股票交割单到excel文件， 每只股票单独一个Excel文件 """

excel_path = r'E:\\OneDrive\\文档\\2、生活口才\\股票交割单\\'
stock_list: List[str] = ['兴业银行']
start_row = 5


def get_text() -> str:
    w.OpenClipboard()
    d = w.GetClipboardData(win32con.CF_TEXT)
    w.CloseClipboard()
    return d.decode('GBK')


# todo 把 main 方法提出为函数


if __name__ == '__main__':
    today = datetime.datetime.today().date().strftime('%Y%m%d')
    c = get_text()
    li = c.split('\r\n')
    for name in stock_list:
        try:
            xlsx = xlwings.Book(excel_path + name + '交割单.xlsx')
            sheet = Sheet(xlsx.sheets[0])
        except:
            continue

        for i in li:
            line = i.split('\t')[0:9]
            if line[0] == today and line[2] == name:
                sheet.api.Rows(start_row).Insert()
                for i in range(1, len(line) + 1):
                    sheet.range(start_row, i).value = line[i - 1]

                # name = line[2] + '交割单.xlsx'
