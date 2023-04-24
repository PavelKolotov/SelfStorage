import telebot


from telebot import types
from environs import Env
from telebot.util import quick_markup


env = Env()
env.read_env()
tg_bot_token = env('TG_CLIENTS_TOKEN')
agreement = env('AGREEMENT')
bot = telebot.TeleBot(token=tg_bot_token)
# rules = env('RULES')
# ADMINS = env.list('ADMINS')

# user groups
UG_ADMIN = 2      # admimnistrators
UG_CLIENT = 1     # clients

# others
INPUT_DUE_TIME = 60     # time (sec) to wait for user text input
BUTTONS_DUE_TIME = 30   # time (sec) to wait for user clicks button
ACCESS_DUE_TIME = 300   # if more time has passed since last main menu we should check access again

# user access status
USER_NOT_FOUND = -1     # user not found in DB
ACCESS_DENIED = 0       # user is found but access is forbidden
ACCESS_ALLOWED = 1      # user is found and access is allowed

# main menu callback buttons
markup_client = quick_markup({
    'Правила хранения': {'callback_data': 'rules_to_client'},
    'Арендовать бокс': {'callback_data': 'rent_to_client'},
    'Моя кладовка': {'callback_data': 'client_pantry'},
})

markup_admin = quick_markup({
    'Просроченное хранение': {'callback_data': 'overdue_storage'},
    'Заказы на хранение': {'callback_data': 'get_storage_orders_id:1'},
    'Заказы на возврат': {'callback_data': 'get_storage_orders_id:4'},
    'Заказы на доставку': {'callback_data': 'get_storage_orders_id:3'},
    'Добавить администратора': {'callback_data': 'add_admin'},
    'Статистика': {'callback_data': 'stats'}
})

# 'return_orders'
# 'return_orders_delivery'

markup_cancel_step = quick_markup({
    'Отмена': {'callback_data': 'cancel_step'},
  })


markup_skip = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
skip = types.KeyboardButton(text='Пропустить')
markup_skip.add(skip)

# markup_accept = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
# reject = types.KeyboardButton(text='Отклонить')
# confirm = types.KeyboardButton(text='Подтвердить')
# menu = types.KeyboardButton(text='Назад в меню')
# markup_accept.add(menu, reject, confirm)

# markup_next = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
# next_ = types.KeyboardButton(text='Вперед')
# back = types.KeyboardButton(text='Назад')
# menu = types.KeyboardButton(text='В меню')
# close = types.KeyboardButton(text='Статус 5')
# fail = types.KeyboardButton(text='Статус 8')
# markup_next.add(menu, back, next_, close, fail)
# markup_skip_or_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
# markup_skip_or_menu.add(menu, skip)

markup_type_rent = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
box = types.KeyboardButton(text='Бокс')
rack = types.KeyboardButton(text='Стеллаж')
markup_type_rent.add(box, rack)

markup_agreement = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
cancel = types.KeyboardButton(text='Отмена')
accept = types.KeyboardButton(text='Принять')
markup_agreement.add(cancel, accept)

# markup_add_admin = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
# markup_add_admin.add(accept, menu)

markup_remove = types.ReplyKeyboardRemove()

chats = {}

rate_box = 1000
rate_rack = 899
rate_weight = 2
