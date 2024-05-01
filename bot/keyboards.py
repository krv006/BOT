from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardBuilder

admin_panel_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='add product'), KeyboardButton(text='add category')],
              [KeyboardButton(text='Category larni korish'), KeyboardButton(text='Produktlarni korish')],
              ],
    resize_keyboard=True)

user_panel_keyboard = ReplyKeyboardMarkup(keyboard=[[
    KeyboardButton(text='Produktlarni korish'), KeyboardButton(text='Category larni korish')
]],
    resize_keyboard=True)
