import asyncio
import logging
import os
import sys
import types
from distutils.cmd import Command
from typing import Any, Union, Dict
from uuid import uuid4

import requests
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Filter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, KeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from dotenv import load_dotenv
from redis_dict import RedisDict

load_dotenv('../env/.env')
TOKEN = os.getenv("TOKEN")  # @yangi123bot
dp = Dispatcher()

database = RedisDict('products')

ADMIN_LIST = 1305675046,

# category = [
#     {
#         'text': 'Texnika',
#         'products': ['63r2t7364', '63r2t7364324']
#     }
# ]

# products = {
#     "63r2t7364": {
#         'name': 'Iphone 4',
#         'price': 400,
#         'quantity': 3,
#         'category': 'Texnika'
#     },
#     "63r2t432327364": {
#         'name': 'Iphone 4',
#         'price': 400,
#         # 'image': 'file_id', # v1
#         'image': 'url',  # v2
#         'quantity': 3,
#         'category': 'Texnika'
#     }
# }

products = {}


class FormState(StatesGroup):
    category = State()
    product_name = State()
    product_price = State()
    product_quantity = State()
    product_image = State()
    product_description = State()
    product_category = State()


def make_url(message: Message, bot: Bot):
    with open('for_url.jpg', 'rb') as f:
        response = requests.post('https://telegra.ph/upload', files={'file': f})
        data = response.json()
        url = "https://telegra.ph" + data[0].get('src').replace(r"\\", '')
    return url


def reaply_keyboard(message: Message, bot: Bot):
    rkb = ReplyKeyboardMarkup()
    for _category in database['category']:
        rkb.add(KeyboardButton(text=_category['texr']))
    rkb.adjust(3, repeat=True)
    return rkb


@dp.message(F.from_user.id.in_(ADMIN_LIST), Command(commands='view_product'))
async def start_for_admin(message: Message):
    rkb = ReplyKeyboardBuilder()
    rkb.add(
        KeyboardButton(text='Category qoshish'),
        KeyboardButton(text='Product qoshish'),
    )
    await message.answer('Tanlang', reply_markup=rkb.as_markup(resize_keyboard=True))
    print(database)


@dp.message((F.from_user.id.in_(ADMIN_LIST)) & (F.text == 'Category qoshish'))
async def add_category(message: Message, state: FSMContext):
    rkb = ReplyKeyboardRemove()
    await state.set_state(FormState.category)
    await message.answer('Category nomini kiriting', reply_markup=rkb)


@dp.message((F.from_user.id.in_(ADMIN_LIST)) & (F.text == 'Product qoshish'))
async def add_product(message: Message, state: FSMContext):
    if not database['category']:
        await message.answer('Avval category kiriting')
        return
    rkb = ReplyKeyboardRemove()
    await state.set_state(FormState.product_name)
    await message.answer('Product nomini kiriting', reply_markup=rkb)


@dp.message(F.from_user.id.in_(ADMIN_LIST), FormState.category)
async def add_category(message: Message, state: FSMContext):
    category = database['category']
    category.append({'text': message.text, 'products': []})
    database['category'] = category
    await state.clear()
    await message.answer('Category qoshildi')


@dp.message(F.from_user.id.in_(ADMIN_LIST), FormState.product_name)
async def add_product(message: Message, state: FSMContext):
    products['name'] = message.text
    await state.set_state(FormState.product_price)
    await message.answer('Product narxini kiriting: ')


@dp.message(F.from_user.id.in_(ADMIN_LIST), FormState.product_price)
async def add_product(message: Message, state: FSMContext):
    products['price'] = message.text
    await state.set_state(FormState.product_quantity)
    await message.answer('Product sonini kiriting: ')


@dp.message(F.from_user.id.in_(ADMIN_LIST), FormState.product_quantity)
async def add_product(message: Message, state: FSMContext):
    products['quantity'] = message.text
    await state.set_state(FormState.product_image)
    await message.answer('Product rasmini kiriting: ')


@dp.message(F.from_user.id.in_(ADMIN_LIST), FormState.product_image)
async def add_product(message: Message, state: FSMContext):
    products['image'] = message.photo[0].file_id
    # products['image_for_users'] = make_url(message)
    await state.set_state(FormState.product_description)
    await message.answer('Product malumotini kiriting: ')


@dp.message(F.from_user.id.in_(ADMIN_LIST), FormState.product_description)
async def add_product(message: Message, state: FSMContext):
    products['description'] = message.text
    rkb = ReplyKeyboardBuilder()
    for _category in database['category']:
        rkb.add(KeyboardButton(text=_category['text']))
    rkb.adjust(3, repeat=True)
    await state.set_state(FormState.product_category)
    await message.answer('Category ni tanlang', reply_markup=rkb.as_markup(resize_keyboard=True))


@dp.message(F.from_user.id.in_(ADMIN_LIST), FormState.product_category)
async def add_product(message: Message, state: FSMContext):
    global products
    products['category'] = message.text
    product_id = str(uuid4())
    products_ = database['products']
    products_[product_id] = products
    categories = database['category']
    for category in categories:
        if category['text'] == message.text:
            category['products'].append(product_id)
    await state.clear()
    await message.answer('Saqlandi', reply_markup=ReplyKeyboardRemove())
    database['products'] = products_
    database['category'] = categories
    print(database)


@dp.message(F.from_user.id.in_(ADMIN_LIST), CommandStart())
async def start_for_admin(message: Message):
    rkb = ReplyKeyboardBuilder()
    rkb.add(
        KeyboardButton(text='Category qoshish'),
        KeyboardButton(text='Product qoshish'),
    )
    await message.answer('Tanlang', reply_markup=rkb.as_markup(resize_keyboard=True))
    print(database)


@dp.message(CommandStart())
async def start(message: Message):
    rkb = ReplyKeyboardBuilder()
    for _category in database['category']:
        rkb.add(KeyboardButton(text=_category['text']))
    rkb.adjust(3, repeat=True)
    await message.answer('Category ni tanlang', reply_markup=rkb.as_markup(resize_keyboard=True))


class IsCategoryFilter(Filter):

    async def __call__(self, message: Message):
        categories: list = database.get('category')
        for category in categories:
            if message.text == category['text']:
                return True
        return False


def get_products(category_name: str):
    products = []
    for product in database['products']:
        if product['category'] == category_name:
            products.append(product)
    return products


@dp.message(IsCategoryFilter())
async def start(message: Message):
    products = get_products(message.text)
    await message.answer(f'{message.text} tanlandi')


@dp.message()
async def start(message: Message):
    await message.answer('togri tanlov emas')


async def on_startup(dispatcher: Dispatcher):
    if not database.get('category'):
        database['category'] = []
    if not database.get('products'):
        database['products'] = {}


async def main() -> None:
    bot = Bot(TOKEN)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

'''
category qoshish va product qoshish

image 2hil saqlansin

1. file_id orqali
2. https://telegra.ph/
https://telegra.ph/api

'''
