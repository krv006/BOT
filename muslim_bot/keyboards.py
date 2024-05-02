from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardBuilder

admin_panel_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Nomoz vaqtini yangilash'), KeyboardButton(text='Register bolgan users lardi korish')],
        # [KeyboardButton(text='Manzilingizdi kiriting'), KeyboardButton(text='Sozlamalar')],
        ],
    resize_keyboard=True)

user_panel_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Nomoz vaqtini korish'), KeyboardButton(text='Qazo nomozlar')],
              [KeyboardButton(text='Manzilingizdi kiriting')],
              [KeyboardButton(text='Registratsiya')],
              ],
    resize_keyboard=True)
