# -*- coding: utf-8 -*-

import os, sqlite3
from typing import List
import win32clipboard as w

import win32con

create_table_sql = """create table check_list (id integer constraint check_list_pk primary key autoincrement,
                        date text, code text, name text, b_s text, quantity int,
                        price decimal(10,4), actual_amount decimal(15,4), available_balance int, contract int); """


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
        line = lines[i].split('\t')[0:14]
        if line[2] is not 'Ｒ-001':
            result.append(line)
    return result


def save_today_stock_check_list(lines: List[List[str]]):
    db_file = r'E:\\OneDrive\\文档\\2、生活口才\\股票交割单\\所有交割单.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    for line in lines:
        value = get_insert_sql(line)
        # print(value)
        cursor.execute(
            'insert into check_list (date, code, name, b_s, quantity, price, actual_amount, available_balance, contract) values' + value)

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


def get_insert_sql(line):
    s2 = ','
    s3 = ',\''
    s1 = '\',\''
    # print(line[2])
    contract_no = s3 if line[13] == '' else (s3 + line[13])
    value = '(\'' + s1.join(line[0:4]) + '\',' + s2.join(line[4:6]) + s2 + line[8] + s2 + line[7] + contract_no + '\')'
    return value


def create_table():
    db_file = r'E:\\OneDrive\\文档\\2、生活口才\\股票交割单\\所有交割单.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(create_table_sql)

    # 通过rowcount获得插入的行数:
    # print('rowcount =', cursor.rowcount)
    # 关闭Cursor:
    cursor.close()
    # 提交事务:
    conn.commit()
    # 关闭Connection:
    conn.close()


# todo 把 main 方法提出为函数
if __name__ == '__main__':
    # create_table()
    save_today_stock_check_list(parse_to_list(get_clipboard()))
