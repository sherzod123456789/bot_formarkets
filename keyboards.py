from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from database import *


def send_contact_button():
    return ReplyKeyboardMarkup([
        [KeyboardButton(text='Поделиться контактом', request_contact=True)]
        # когда в тг приходит запрос, можно ли отправить контакты
    ], resize_keyboard=True)  # resize_keyboard делает кнопку меньше


def generate_main_menu():
    return ReplyKeyboardMarkup([
        [KeyboardButton(text='✔Сделать заказ')],
        [KeyboardButton(text='📓История'), KeyboardButton(text='🛒Корзина'), KeyboardButton(text='⚙Настройки'),
         ]
    ], resize_keyboard=True)


def generate_category_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.row(
        InlineKeyboardMarkup(text='Все меню', url='https://davidlazba.com/lion')
    )
    categories = get_all_categories()  # Для получения всех категорий товаров
    button = []
    for category in categories:
        btn = InlineKeyboardButton(text=category[1], callback_data=f'category_{category[0]}')
        button.append(btn)

    markup.add(*button)
    markup.row(
        InlineKeyboardButton(text='⬅ Назад', callback_data='main_menu')
    )
    return markup


def generate_products_by_category(category_id):
    markup = InlineKeyboardMarkup(row_width=2)
    products = get_products_by_category_id(category_id)
    buttons = []
    for product in products:
        btn = InlineKeyboardButton(text=product[1], callback_data=f'product_{product[0]}')
        buttons.append(btn)
    markup.add(*buttons)
    markup.row(
        InlineKeyboardButton(text='⬅ Назад', callback_data='main_menu')
    )
    return markup


def generate_product_detail_menu(product_id, category_id,
                                 cart_id, product_name='', c=0):
    markup = InlineKeyboardMarkup(row_width=2)
    try:
        quantity = get_quantity(cart_id, product_name)
    except:
        quantity = c

    buttons = []
    btn_minus = InlineKeyboardButton(text=str('➖'), callback_data=f'minus_{quantity}_{product_id}')
    btn_plus = InlineKeyboardButton(text=str(quantity), callback_data=f'coll')
    btn_quantity = InlineKeyboardButton(text=str('➕'), callback_data=f'plus_{quantity}_{product_id}')
    buttons.append(btn_minus)
    buttons.append(btn_quantity)
    buttons.append(btn_plus)
    markup.add(*buttons)
    markup.row(
        InlineKeyboardButton(text='🛒Добавить в корзину', callback_data=f'cart_{product_id}_{quantity}')
    )
    markup.row(
        InlineKeyboardButton(text='◀Назад', callback_data=f'back_{category_id}')
    )
    return markup

def generate_cart_menu(cart_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.row(
        InlineKeyboardButton(text='Оформить заказ', callback_data=f'order_{cart_id}')
    )
    cart_products = get_cart_products_for_delete(cart_id)

