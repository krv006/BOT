from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

import keyboards as kb
from config import ADMIN, product_scheme, category_db, product_db

main_router = Router()


@main_router.message(CommandStart())
async def start(message: Message):
    if str(message.from_user.id) == ADMIN:
        await message.answer('Siz adminsiz!')
        await message.answer('Tanlang', reply_markup=kb.admin_panel_keyboard)
    else:
        await message.answer('Hello user')
        await message.answer('Tanlang', reply_markup=kb.user_panel_keyboard)


class AddProduct(StatesGroup):
    id = State()
    title = State()
    description = State()
    price = State()
    brand = State()
    category = State()
    thumbnail = State()
    quantity = State()


@main_router.message(F.text == 'add product')
async def add_product(message: Message, state: FSMContext):
    if str(message.from_user.id) == ADMIN:
        await state.set_state(AddProduct.id)
        await message.answer('Id kiriting:')


@main_router.message(AddProduct.id)
async def add_product(message: Message, state: FSMContext):
    if str(message.from_user.id) == ADMIN:
        await state.update_data(id=message.text)
        await state.set_state(AddProduct.title)
        await message.answer('Title kiriting:')


@main_router.message(AddProduct.title)
async def add_product(message: Message, state: FSMContext):
    if str(message.from_user.id) == ADMIN:
        await state.update_data(title=message.text)
        await state.set_state(AddProduct.description)
        await message.answer('Description kiriting:')


@main_router.message(AddProduct.description)
async def add_product(message: Message, state: FSMContext):
    if str(message.from_user.id) == ADMIN:
        await state.update_data(description=message.text)
        await state.set_state(AddProduct.price)
        await message.answer('Price kiriting:')


@main_router.message(AddProduct.price)
async def add_product(message: Message, state: FSMContext):
    if str(message.from_user.id) == ADMIN:
        await state.update_data(price=message.text)
        await state.set_state(AddProduct.brand)
        await message.answer('Brand kiriting:')


@main_router.message(AddProduct.brand)
async def add_product(message: Message, state: FSMContext):
    if str(message.from_user.id) == ADMIN:
        await state.update_data(brand=message.text)
        await state.set_state(AddProduct.category)
        await message.answer('Category kiriting:')


@main_router.message(AddProduct.category)
async def add_product(message: Message, state: FSMContext):
    if str(message.from_user.id) == ADMIN:
        await state.update_data(category=message.text)
        await state.set_state(AddProduct.thumbnail)
        await message.answer('Thumbnail kiriting:')


@main_router.message(AddProduct.thumbnail)
async def add_product(message: Message, state: FSMContext):
    if str(message.from_user.id) == ADMIN:
        img = message.photo[0].file_id
        await state.update_data(thumbnail=img)
        await state.set_state(AddProduct.quantity)
        await message.answer('Quantity kiriting:')


@main_router.message(AddProduct.quantity)
async def add_product(message: Message, state: FSMContext):
    if str(message.from_user.id) == ADMIN:
        await state.update_data(quantity=message.text)
        data = await state.get_data()
        await state.clear()
        text = f""" Everything correct?
                Product id: {data.get('id')}"
                Product title: {data.get('title')}
                Product description: {data.get('description')}
                Product price: {data.get('price')}
                Product brand: {data.get('brand')}
                Category id: {data.get('category')}
                Thumbnail: {data.get('thumbnail')}
                Quantity: {data.get('quantity')}"""
        await product_scheme(data)
        await message.answer('Saqlandi!')


class AddCategory(StatesGroup):
    category_name = State()


@main_router.message(F.text == 'add category')
async def add_category(message: Message, state: FSMContext):
    if str(message.from_user.id) == ADMIN:
        await state.set_state(AddCategory.category_name)
        await message.answer('Category kiriting:')


@main_router.message(AddCategory.category_name)
async def add_category(message: Message, state: FSMContext):
    if str(message.from_user.id) == ADMIN:
        await state.update_data(category_name=message.text)
        data = await state.get_data()
        await state.clear()
        category_db[data['category_name']] = True
        await message.answer('Category qoshildi!')


@main_router.message(F.text == 'Category larni korish')
async def show_categories(message: Message):
    rkb = ReplyKeyboardBuilder()
    for category in category_db:
        rkb.row(KeyboardButton(text=category))
    rkb.row(KeyboardButton(text='ortga'))
    rkb.adjust(3)
    await message.answer('Tanlang...', reply_markup=rkb.as_markup(resize_keyboard=True))


@main_router.message(F.text.in_(category_db))
async def pocc(message: Message):
    ikb = InlineKeyboardBuilder()
    for product in product_db:
        if product_db[product]['category'] == message.text:
            ikb.row(InlineKeyboardButton(text=product_db[product]['title'],
                                         callback_data=product_db[product]['title']))
    ikb.row(InlineKeyboardButton(text='❌', callback_data='delete'),
            InlineKeyboardButton(text='Search 🔍', callback_data='search'))
    ikb.adjust(2)
    await message.answer(f"products of {message.text} category.", reply_markup=ikb.as_markup())


@main_router.callback_query(F.data == 'delete')
async def delete(callback: CallbackQuery, bot: Bot):
    if str(callback.message.from_user.id) == ADMIN:
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        await callback.message.answer('Tanlang...', reply_markup=kb.admin_panel_keyboard)
    else:
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        await callback.message.answer('Tanlang...', reply_markup=kb.user_panel_keyboard)



@main_router.message(F.text == 'ortga')
async def ortga(message: Message):
    if str(message.from_user.id) == ADMIN:
        await message.answer('Tanlang...', reply_markup=kb.admin_panel_keyboard)
    else:
        await message.answer('Tanlang...', reply_markup=kb.user_panel_keyboard)


@main_router.message(F.photo)
async def photo(message: Message):
    await message.answer(message.text)