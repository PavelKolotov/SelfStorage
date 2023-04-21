import sqlite3
from datetime import datetime, timedelta

from globals import USER_NOT_FOUND, ACCESS_DENIED, ACCESS_ALLOWED



def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


con = sqlite3.connect("database.db", check_same_thread=False)
con.row_factory = dict_factory


#Пример работы с БД

def get_example(user_id):
    cur: sqlite3.Cursor = con.execute(f'select * from orders where client_id="{user_id}"')
    row = cur.fetchone()
    cur.close()
    return row

example = get_example(933137433)

print(example)
print(example['client_address'])

def get_user_by_chat_id(chat_id):
    cur: sqlite3.Cursor = con.execute(f'select *  from users where tg_user_id={chat_id}')
    row = cur.fetchone()
    cur.close()
    return row


def check_user_access(tg_name=None, tg_user_id=None):
    '''проверяет наличие доступа к системе у пользователя с указанным именем.
    (имеется ввиду имя пользователя в Telegram)
    Возвращает кортеж (а, б), где а=-1 - пользователя нет в БД.
    а=0 - пользователь есть в БД, но нет доступа
    а=1 - пользователь есть в БД и обладает доступом
    б - код группы пользователя (0-админы, 1-клиенты)
    '''
    cur: sqlite3.Cursor = con.execute(f"select access, user_group "
                                      f"from users where tg_name='{tg_name if tg_name else 0}' or "
                                      f"tg_user_id={tg_user_id if tg_user_id else 0}"
                                      )
    row = cur.fetchone()
    cur.close()
    if not row:
        return (USER_NOT_FOUND, None)
    elif row['access']:
        return (ACCESS_ALLOWED, row['user_group'])
    else:
        return (ACCESS_DENIED, row['user_group'])


def add_new_user(name, phone, tg_name, tg_user_id, user_group=1, access=1):
    data = (name, phone, tg_name, tg_user_id, user_group, access)
    cur = con.execute(
        'insert into users '
        '(name, phone, tg_name, tg_user_id, user_group, access) '
        'values( ?, ?, ?, ?, ?, ?)', data)
    con.commit()
    cur.close()
    return cur.lastrowid

def add_new_order(client_id, value, weight, date_reg, shelf_life,
                  client_address, client_phone, inventory=None,
                  box_number=None, rack_number=None,
                  forwarder_id=0, status=1):
    #  ' Отредактировать в соответствии с колонками таблицы ' #
    date_end = date_reg + timedelta(days=shelf_life*30)
    order_id = len(get_orders(client_id))

    alert_date = date_end - timedelta(days=10)  # need redact
    data = (order_id, client_id, forwarder_id, client_phone, client_address,
            box_number, rack_number, value, weight, shelf_life,
            date_reg, date_end, alert_date, status, inventory)

    cur = con.execute(
        'insert into orders '
        '''(order_id, client_id, forwarder_id, client_phone, client_address, box_number, 
        rack_number, value, weight, shelf_life, date_reg, date_end, alert_date, status, inventory) '''
        'values( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data)

    con.commit()
    cur.close()
    return cur.lastrowid


def update_order(user_id, order_id, data):
    order = get_orders(user_id)[order_id]
    order.update(data)
    order = convert_dict(order)
    cur = con.execute(
        f"update orders set {order} "
        )

    con.commit()
    cur.close()
    return cur.lastrowid


def get_orders(user_id):
    cur: sqlite3.Cursor = con.execute(f'select * from orders where client_id="{user_id}"')
    row = cur.fetchall()
    cur.close()
    return row


def convert_dict(dictionary):
    string = ''
    for item, value in dictionary.items():
        part = f"{item} = '{value}', "
        string += part
    return string[:-2]



# name = 'test'
# phone = 111
# tg_name = 'test_name'
# tg_user_id = 7
# value = 1234
# weight = 56
# now = datetime.now()
# date_reg = now
# shelf_life = 78
# date_end = now + timedelta(days=shelf_life)
# client_address = 'test address'

# # check all orders
# print(get_orders(tg_user_id))
# # create new order
# add_new_order(tg_user_id, value, weight, date_reg, shelf_life, client_address, phone)
# # print(get_orders(tg_user_id))
# # update order
# update_data = {}  # for dict.update
# latest = get_orders(tg_user_id)[-1]['order_id']
# update_order(tg_user_id, latest, update_data)
# # check latest order
# print(get_orders(tg_user_id)[-1])