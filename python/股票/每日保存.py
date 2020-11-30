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
        self.date_idx = None
        self.time_idx = None
        self.code_idx = None
        self.name_idx = None
        self.bs_idx = None
        self.quantity_idx = None
        self.price_idx = None
        self.actual_amount_idx = None
        self.amount_idx = None
        self.available_balance_idx = None
        self.contract_idx = None


class CheckItem:
    def __init__(self, date: str = None, time: str = None, code: str = None, name: str = None,
                 bs: str = None, quantity: int = None, price: float = None, available_balance: int = None,
                 contract: str = None):
        self.date = date
        self.time = time
        self.code = code
        self.name = name
        self.bs = bs  # 买或卖
        self.quantity = quantity  # 成交量
        self.price = price  # 成交价格
        self.actual_amount = -1  # 实际发生金额
        self.amount = -1  # 成交金额
        self.available_balance = available_balance  # 可用余额(数量)
        self.contract = contract  # 合同号

    def __str__(self):
        return self.date + ' ' + self.time


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


def get_check_item(idxes: DataIndex, li: List[str]) -> CheckItem:
    available_balance = int(li[idxes.available_balance_idx]) if idxes.available_balance_idx else None
    a = CheckItem(date=li[idxes.date_idx], time=li[idxes.time_idx], code=li[idxes.code_idx], name=li[idxes.name_idx],
                  bs=li[idxes.bs_idx], quantity=int(li[idxes.quantity_idx]), price=float(li[idxes.price_idx]),
                  available_balance=available_balance, contract=li[idxes.contract_idx])
    amount = a.price * a.actual_amount
    if a.bs == '买':
        # 佣金: 双向收费, 看券商     过户费: 双向收费 0.00002    印花税: 卖时收费 0.001
        a.actual_amount = -amount - round(amount * 0.0001, 2) - round(amount * 0.00002, 2)
    elif a.bs == '卖':
        a.actual_amount = amount - round(amount * 0.0001, 2) - round(amount * 0.00002, 2) - round(amount * 0.001, 2)
    return a


def parse_to_list(clip: str) -> List[CheckItem]:
    if '成交日期' not in clip or '\r\n' not in clip or '成交时间' not in clip or '\t' not in clip:
        print("剪贴板没有成交记录")
        return []
    lines = clip.split('\r\n')
    data_idx = get_index(lines[0].split('\t')[0:14])
    result = []
    for i in range(1, len(lines)):
        line = lines[i].split('\t')[0:14]
        if line[data_idx.code_idx] is not 'Ｒ-001':
            result.append(get_check_item(data_idx, line))
    result.sort(key=lambda x: x.date + x.time)
    return result


def save_today_stock_check_list(lines: List[CheckItem]):
    if not lines:
        return
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    for item in lines[1:]:
        sql = get_insert_sql(item)
        cursor.execute('select * from check_list where date=\'' + item.date + '\' and contract=\'' + item.contract + '\'')
        v = cursor.fetchall()
        # todo 根据日期和合同号判断数据库中是否已经保存过了
        if not v and len(v) == 0:
            cursor.execute(sql)

    # 通过rowcount获得插入的行数:
    # print('rowcount =', cursor.rowcount)
    cursor.close()
    conn.commit()
    conn.close()


def get_insert_sql(item: CheckItem):
    s1 = '\',\''
    s2 = '\','
    s3 = ','
    sql_value = '(\'' + item.date
    sql_value = (sql_value + s1 + item.time) if item.time else (sql_value + s1)
    sql_value = sql_value + s1 + item.code + s1 + item.name + s1 + item.bs + s2
    sql_value = sql_value + str(item.quantity) + s3 + str(item.price) + s3 + str(item.actual_amount) + s3
    sql_value = (sql_value + str(item.available_balance)) if item.available_balance else sql_value + 'null'
    sql_value = (sql_value + ',\'' + item.contract + '\')') if item.contract else (sql_value + ',\'\')')
    sql = "insert into check_list (date, time, code, name, b_s, quantity, price, actual_amount, available_balance, contract) values" + sql_value
    return sql


def create_table():
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
            sql = 'update check_list set time=\'' + line[data_idx.time_idx] + '\' where date=\'' + line[data_idx.date_idx] + '\' and contract=\'' + contract + '\''
            cursor.execute(sql)

    # cursor.execute('select id ')
    cursor.close()
    conn.commit()
    conn.close()


if __name__ == '__main__':
    # create_table()
    # update_deal_time()
    # save_today_stock_check_list(parse_to_list(get_clipboard()))
    l =parse_to_list(get_clipboard())
    for i in l:
        print(i)

