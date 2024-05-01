from aiogram import Router, F
from aiogram.types import InlineKeyboardButton, URLInputFile, Message, CallbackQuery, InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import product_db

pagination_router = Router()

BASE_URL = 'https://dummyjson.com/products'


def make_inline_button(product):
    ikb = InlineKeyboardBuilder()
    ikb.row(
        InlineKeyboardButton(text='<', callback_data=str(int(product['id']) - 1)),
        InlineKeyboardButton(text=f"{product['id']}/{len(product_db)}", callback_data=f"current_{product['id']}"),
        InlineKeyboardButton(text='>', callback_data=str(int(product['id']) + 1))
    )
    return ikb.as_markup()


@pagination_router.message(F.text == 'Produktlarni korish')
async def pagination_start(message: Message):
    if product_db:
        product = product_db[1]
        text = f"<b>{product['title']}</b>\n\n{product['description']}"
        img = product['thumbnail']
        await message.answer_photo(img, caption=text, reply_markup=make_inline_button(product))
    else:
        await message.answer('There are no products in database')


@pagination_router.callback_query(F.data.func(lambda data: data.isdigit() or data.startswith('current_')))
async def start(callback: CallbackQuery):
    if callback.data.startswith('current_'):
        current_product_id = callback.data.split('_')[-1]
        text = current_product_id
        await callback.answer(text, show_alert=True)

    elif callback.data.isdigit():
        if not (product_db[callback.data]):
            await callback.answer('Limit', show_alert=True)

        else:
            product = product_db[callback.data]
            text = f"<b>{product['title']}</b>\n\n{product['description']}"
            img = product['thumbnail']
            media = InputMediaPhoto(media=img, caption=text)
            await callback.message.edit_media(media, reply_markup=make_inline_button(product))