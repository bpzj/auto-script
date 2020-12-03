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
                 actual_amount: float = 0, amount: float = 0, contract: str = None):
        self.date = date
        self.time = time
        self.code = code
        self.name = name
        self.bs = bs  # 买或卖
        self.quantity = quantity  # 成交量
        self.price = price  # 成交价格
        self.actual_amount = actual_amount  # 实际发生金额
        self.amount = amount  # 成交金额
        self.available_balance = available_balance  # 可用余额(数量)
        self.contract = contract  # 合同号

    def __str__(self):
        return self.date + ' ' + self.time + ' ' + self.code + ' ' + self.name + ' ' + self.bs + ' ' + str(
            round(self.actual_amount, 2))


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


def get_clipboard() -> List[List[str]]:
    w.OpenClipboard()
    d = w.GetClipboardData(win32con.CF_TEXT)
    w.CloseClipboard()
    clip = d.decode('GBK')
    if '成交日期' not in clip or '\r\n' not in clip or '\t' not in clip:
        print("剪贴板没有成交记录")
        exit(-1)
    lines = clip.split('\r\n')
    result = []
    for a in lines:
        result.append(a.split('\t')[0:14])
    return result


def get_check_item(idxes: DataIndex, li: List[str]) -> CheckItem:
    a = CheckItem(date=li[idxes.date_idx], time=li[idxes.time_idx], code=li[idxes.code_idx], name=li[idxes.name_idx],
                  bs=li[idxes.bs_idx], quantity=int(li[idxes.quantity_idx]), price=float(li[idxes.price_idx]),
                  amount=float(li[idxes.amount_idx]), contract=li[idxes.contract_idx])
    if a.amount == 0:
        a.actual_amount = 0
        return a
    if a.quantity == 0 and a.amount > 0 and a.bs == '买':
        a.actual_amount = - a.amount
        return a
    佣金 = round(a.amount * 0.0001, 2)  # 佣金: 双向收费, 看券商
    过户费 = round(a.amount * 0.00002, 2)  # 过户费: 双向收费 0.00002  ETF不收
    印花税 = round(a.amount * 0.001, 2)  # 印花税: 卖时收费 0.001    ETF不收
    if a.bs == '买':
        if a.code.startswith('15') or a.code.startswith('51'):
            a.actual_amount = -a.amount - 佣金  # ETF 不收过户费
        else:
            a.actual_amount = -a.amount - 过户费 - 佣金
    elif a.bs == '卖':
        if a.code.startswith('15') or a.code.startswith('51'):
            a.actual_amount = a.amount - 佣金  # ETF 不收过户费
        else:
            a.actual_amount = a.amount - 过户费 - 佣金 - 印花税
    elif a.bs == '配':
        a.actual_amount = -a.amount
    return a


def 更改配债配股(data_idx, line, lines: List[List[str]]):
    """获取配债配股的股票代码"""
    date = line[data_idx.date_idx]
    quantity = line[data_idx.quantity_idx]
    for li in lines:
        if li[data_idx.date_idx] == date and li[data_idx.bs_idx] == '买' and li[data_idx.quantity_idx] == quantity:
            line[data_idx.code_idx] = li[data_idx.code_idx]
            line[data_idx.name_idx] = line[data_idx.name_idx].replace('配债', '转债')
            # line[data_idx.bs_idx] = '买'


def parse_to_list(str_list: List[List[str]]) -> List[CheckItem]:
    data_idx = get_index(str_list[0])
    result = []
    for line in str_list[1:]:
        name = line[data_idx.name_idx]
        if name != 'Ｒ-001' and name != '新增证券' and name != '登记指定':
            # if (line[data_idx.bs_idx]) == '配':
            #     更改配债配股(data_idx, line, str_list)
            result.append(get_check_item(data_idx, line))
    result.sort(key=lambda x: (x.date + x.time) if x.time != '' else (x.date + '99'))
    return result


def save_today_stock_check_list(lines: List[CheckItem]):
    if not lines:
        return
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    for item in lines:
        sql = get_insert_sql(item)
        cursor.execute(
            'select id from check_list where date=\'' + item.date + '\' and contract=\'' + item.contract + '\'')
        v, = cursor.fetchone()
        # todo 根据日期和合同号判断数据库中是否已经保存过了
        if v:
            print('已存在记录')
        else:
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
    sql_value = sql_value + str(item.quantity) + s3 + str(item.price) + s3 + str(round(item.actual_amount, 2)) + s3
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


def get_update(idxes: DataIndex, li: List[str]) -> CheckItem:
    a = CheckItem(date=li[idxes.date_idx], code=li[idxes.code_idx], name=li[idxes.name_idx],
                  bs=li[idxes.bs_idx], actual_amount=float(li[idxes.actual_amount_idx]),
                  available_balance=int(li[idxes.available_balance_idx]), contract=li[idxes.contract_idx])
    return a


def parse_update(str_list: List[List[str]]) -> List[CheckItem]:
    data_idx = get_index(str_list[0])
    if not data_idx.actual_amount_idx or not data_idx.available_balance_idx or not data_idx.contract_idx:
        print('剪切板内容不是交割单')
    result = []
    for line in str_list[1:]:
        name = line[data_idx.name_idx]
        if name != 'Ｒ-001' and name != '新增证券' and name != '登记指定':
            result.append(get_update(data_idx, line))
    return result


def update_available_balance_and_actual_amount(item_list: List[CheckItem]):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    for item in item_list:
        contract = item.contract
        if contract != '':
            sql = 'update check_list set actual_amount=' + str(item.actual_amount) \
                  + ', available_balance=' + str(item.available_balance) \
                  + ' where date=\'' + item.date + '\' and contract=\'' + contract + '\''
            # print(sql)
            cursor.execute(sql)

    # cursor.execute('select id ')
    cursor.close()
    conn.commit()
    conn.close()


def summary():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('select code,name from check_list group by code')
    v = cursor.fetchall()
    for code, name in v:
        cursor.execute(
            'select available_balance from check_list where code=\'' + code + '\' and quantity!=0 order by id desc limit 1')
        available_balance, = cursor.fetchone()
        cursor.execute('select round(sum(actual_amount),2) from check_list where code=\'' + code + '\'')
        sum, = cursor.fetchone()
        if available_balance == 0:
            print(name + ' \t盈亏 ' + str(sum))
        else:
            # todo
            print(name + ' \t成本 ' + str(round(-sum / available_balance, 2)))

    cursor.close()
    conn.commit()
    conn.close()


if __name__ == '__main__':
    # create_table()
    # save_today_stock_check_list(parse_to_list(get_clipboard()))
    # update_available_balance_and_actual_amount(parse_update(get_clipboard()))
    summary()
