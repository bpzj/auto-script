# -*- coding: utf-8 -*-

import os, sqlite3
from typing import List
import win32clipboard as w

import win32con

create_table_sql = """create table check_list (id integer constraint check_list_pk primary key autoincrement,
                        deal_date text, code text, name text, b_s text, quantity int,
                        price numeric, actual_amount numeric, available_balance int); """


def get_clipboard() -> str:
    w.OpenClipboard()
    d = w.GetClipboardData(win32con.CF_TEXT)
    w.CloseClipboard()
    return d.decode('GBK')


def parse_to_list(clip: str) -> List[List[str]]:
    if "成交日期" not in clip:
        # todo 抛出异常
        return None;
    lines = clip.split('\r\n')
    result = []
    for i in range(1, len(lines)):
        result.append(lines[i].split('\t')[0:9])
    return result


def save_today_stock_check_list(lines: List[List[str]]):
    db_file = r'E:\\OneDrive\\文档\\2、生活口才\\股票交割单\\所有交割单.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    s1 = '\',\''
    s2 = ','
    for line in lines:
        value = '(\'' + line[0] + s1 + line[1] + s1 + line[2] + s1 + line[3] + '\'' + \
                s2 + line[4] + s2 + line[5] + s2 + line[8] + s2 + line[7] + ')'
        cursor.execute(
            'insert into check_list (deal_date, code, name, b_s, quantity, price, actual_amount, available_balance) values' + value)

    # 通过rowcount获得插入的行数:
    # print('rowcount =', cursor.rowcount)
    # 关闭Cursor:
    cursor.close()
    # 提交事务:
    conn.commit()
    # 关闭Connection:
    conn.close()
    #
    # for line in lines:
    #     if line[0] <= day and line[2] == name:
    #         sheet.api.Rows(start_row).Insert()
    #         for i in range(1, len(line) + 1):
    #             sheet.range(start_row, i).value = line[i - 1]
    #
    #         if line[3] == '卖':
    #             sheet.range(start_row, 10).value = '-' + line[4]
    #         else:
    #             sheet.range(start_row, 10).value = line[4]
    # name = line[2] + '交割单.xlsx'


# todo 把 main 方法提出为函数
if __name__ == '__main__':
    save_today_stock_check_list(parse_to_list(get_clipboard()))
