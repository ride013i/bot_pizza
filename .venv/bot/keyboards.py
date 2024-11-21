from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from requests import get_menu
from tenacity import retry_unless_exception_type

register_profile = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Зарегистрироваться')]
], resize_keyboard=True) #TODO Разобратся с цветом клавиатуры, в темной теме

main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Меню'), KeyboardButton(text='Корзина')],
    [KeyboardButton(text='Настройки')]
], resize_keyboard=True)

cart_user = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Отправить заказ')],
    [KeyboardButton(text='Очистить корзину'), KeyboardButton(text='Назад')]
], resize_keyboard=True)

settings = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Профиль'), KeyboardButton(text='Изменить профиль')],
    [KeyboardButton(text='Назад')]
], resize_keyboard=True)

send_contact = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Отправить контакт', request_contact=True)]
], resize_keyboard=True)

send_location = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Отправить локацию', request_location=True)]
], resize_keyboard=True)

# Функция сборки инлайн клавиатуры-меню работает для всех
async def menu():
    all_menu = await get_menu()
    keyboard = InlineKeyboardBuilder()
    for menu in all_menu:
        print(menu.id)
        keyboard.add(InlineKeyboardButton(text=menu.name, callback_data=f'pizza_{menu.id}'))
    return keyboard.adjust(1).as_markup()

# # Функция сборки инлайн клавиатуры-корзины пользователя
async def cart(user_id):
    all_cart = await get_cart(user_id=user_id)
    keyboard = InlineKeyboardBuilder()
    for cart in all_cart:
        keyboard.add(InlineKeyboardButton(text=cart.name, callback_data=f'cart_{cart.id}'))
    return keyboard.adjust(1).as_markup()