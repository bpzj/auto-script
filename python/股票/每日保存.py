# -*- coding: utf-8 -*-

import sqlite3
from typing import List

import win32clipboard as w
import win32con

db_file = r'E:\\OneDrive\\文档\\2、生活口才\\股票交割单\\所有交割单.db'
create_table_sql = """create table check_list (id integer constraint check_list_pk primary key autoincrement,
                        date text, code text, name text, b_s text, quantity int,
                        price decimal(10,4), actual_amount decimal(15,4), available_balance int, contract int); """


class DataIndex:
    def __init__(self):
        self.date_idx = -1
        self.time_idx = -1
        self.code_idx = -1
        self.name_idx = -1
        self.bs_idx = -1
        self.quantity_idx = -1
        self.price_idx = -1
        self.actual_amount_idx = -1
        self.amount_idx = -1
        self.available_balance_idx = -1
        self.contract_idx = -1


def get_index(li: List[str]) -> DataIndex:
    idx = DataIndex()
    for i in range(0, len(li)):
        line = li[i]
        if line == '成交日期':
            idx.date_idx = i
        elif line == '成交时间':
            idx.time_idx = i
        elif line == '证券代码':
            idx.code_idx = i
        elif line == '证券名称':
            idx.name_idx = i
        elif line == '操作':
            idx.bs_idx = i
        elif line == '成交数量':
            idx.quantity_idx = i
        elif line == '成交均价':
            idx.price_idx = i
        elif line == '成交金额':
            idx.amount_idx = i
        elif line == '发生金额':
            idx.actual_amount_idx = i
        elif line == '可用余额':
            idx.available_balance_idx = i
        elif line == '合同编号':
            idx.contract_idx = i

    return idx


def get_clipboard() -> str:
    w.OpenClipboard()
    d = w.GetClipboardData(win32con.CF_TEXT)
    w.CloseClipboard()
    return d.decode('GBK')


def parse_to_list(clip: str) -> List[List[str]]:
    if "成交日期" not in clip or "\r\n" not in clip:
        # todo 抛出异常
        return []
    lines = clip.split('\r\n')
    result = []
    for i in range(0, len(lines)):
        line = lines[i].split('\t')[0:14]
        if line[2] is not 'Ｒ-001':
            result.append(line)
    return result


def save_today_stock_check_list(lines: List[List[str]]):
    if not lines:
        return
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    data_idx = get_index(lines[0])
    for line in lines[1:]:
        sql = get_insert_sql(data_idx, line)
        # todo 根据日期和合同号判断数据库中是否已经保存过了
        cursor.execute('select * from check_list where date=\'' + line[data_idx.date_idx] + '\' and contract=\'' + line[
            data_idx.contract_idx] + '\'')
        v = cursor.fetchall()
        if not v and len(v) == 0:
            print(v)
            cursor.execute(sql)

    # 通过rowcount获得插入的行数:
    # print('rowcount =', cursor.rowcount)
    cursor.close()
    conn.commit()
    conn.close()


def get_insert_sql(data_idx: DataIndex, line: List[str]):
    date = line[data_idx.date_idx]
    code = line[data_idx.code_idx]
    name = line[data_idx.name_idx]
    b_s = line[data_idx.bs_idx]
    quantity = line[data_idx.quantity_idx]
    price = line[data_idx.price_idx]
    if data_idx.actual_amount_idx:
        actual_amount = line[data_idx.actual_amount_idx]
    else:
        # todo 真实金额
        actual_amount = quantity * float(price)
    if data_idx.available_balance_idx >= 0:
        available_balance = line[data_idx.available_balance_idx]
    time = line[data_idx.time_idx] if data_idx.time_idx >= 0 else None
    contract = line[data_idx.contract_idx] if data_idx.contract_idx >= 0 else ''
    s1 = '\',\''
    s2 = '\','
    s3 = ','
    sql_value = '(\'' + date
    sql_value = (sql_value + s1 + time) if time else (sql_value + s1)
    sql_value = sql_value + s1 + code + s1 + name + s1 + b_s + s2
    sql_value = sql_value + quantity + s3 + price + s3 + actual_amount + s3 + available_balance
    sql_value = (sql_value + ',\'' + contract + '\')') if contract else (sql_value + ',\'\')')
    sql = "insert into check_list (date, time, code, name, b_s, quantity, price, actual_amount, available_balance, contract) values" + sql_value
    return sql


def create_table():
    db_file = r'E:\\OneDrive\\文档\\2、生活口才\\股票交割单\\所有交割单.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(create_table_sql)
    cursor.close()
    conn.commit()
    conn.close()


def update_deal_time():
    li = parse_to_list(get_clipboard())
    data_idx = get_index(li[0])
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    for line in li[1:]:
        contract = line[data_idx.contract_idx]
        if contract != '':
            sql = 'update check_list set time=\'' + line[data_idx.time_idx] + '\' where date=\'' + line[data_idx.date_idx] + '\' and contract=\'' + contract +'\''
            cursor.execute(sql)

    # cursor.execute('select id ')
    cursor.close()
    conn.commit()
    conn.close()


if __name__ == '__main__':
    # create_table()
    update_deal_time()
    # save_today_stock_check_list(parse_to_list(get_clipboard()))
