from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardBuilder

admin_panel_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='📚 Kitoblar')],
              [KeyboardButton(text='📃 Mening buyurtmalarim')],
              [KeyboardButton(text='🔵 Biz ijtimoyi tarmoqlarda'), KeyboardButton(text='📞 Biz bilan bog\'lanish')],
              [KeyboardButton(text='add product'), KeyboardButton(text='add category')],
              [KeyboardButton(text='Category larni korish'), KeyboardButton(text='Produktlarni korish')],
              ],
    resize_keyboard=True)


user_panel_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='📚 Kitoblar')],
    [KeyboardButton(text='📃 Mening buyurtmalarim')],
    [KeyboardButton(text='🔵 Biz ijtimoyi tarmoqlarda'), KeyboardButton(text='📞 Biz bilan bog\'lanish')],
],
    resize_keyboard=True)