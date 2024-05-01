from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardBuilder, InlineKeyboardButton, \
    InlineKeyboardMarkup

admin_panel_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='add product'),
               [KeyboardButton(text='add category')],
               ]],
    resize_keyboard=True)

user_panel_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='show all product'),
               [KeyboardButton(text='show all category')],
               ]],
    resize_keyboard=True)

yes_or_no = InlineKeyboardMarkup(
    keyboard=[[InlineKeyboardButton(text='yes'),
               [InlineKeyboardButton(text='no')],
               ]],
    resize_keyboard=True)
