from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

import keyboards as kb
from config import ADMIN, book_scheme, category_db, product_db

main_router = Router()


@main_router.message(CommandStart())
async def start(message: Message):
    if str(message.from_user.id) == ADMIN:
        await message.answer('Siz adminsiz!')
        await message.answer('Tanlang', reply_markup=kb.admin_panel_keyboard)
    else:
        await message.answer('Hello user')
        await message.answer('Tanlang', reply_markup=kb.user_panel_keyboard)


@main_router.message(F.text == "📞 Biz bilan bog\'lanish")
async def books(message: Message) -> None:
    text = f"""
    Telegram: @factorbooks_info\n
    Murojat uchun 📞 : +{998901078055}\n
    🤖 Bot Rustamov Kamron (@kamron_rustamov_dev) tomonidan tayyorlandi.
        """
    await message.answer(text)


@main_router.message(F.text == "🔵 Biz ijtimoyi tarmoqlarda")
async def books(message: Message) -> None:
    ikb = InlineKeyboardBuilder()
    ikb.row(InlineKeyboardButton(text="Ikar_factor", url="https://t.me/ikar_factor"))
    ikb.row(InlineKeyboardButton(text="Factor_books", url="https://t.me/factor_books"))

    await message.answer("Biz ijtimoyi tarmoqlarda ham kuzatishingiz mumkin", reply_markup=ikb.as_markup())


class AddProduct(StatesGroup):
    id = State()
    title = State()
    text = State()
    price = State()
    quantity = State()
    image = State()
    category = State()


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
        await state.set_state(AddProduct.text)
        await message.answer('Text kiriting:')


@main_router.message(AddProduct.text)
async def add_product(message: Message, state: FSMContext):
    if str(message.from_user.id) == ADMIN:
        await state.update_data(text=message.text)
        await state.set_state(AddProduct.price)
        await message.answer('Narxini kiriting:')


@main_router.message(AddProduct.price)
async def add_product(message: Message, state: FSMContext):
    if str(message.from_user.id) == ADMIN:
        await state.update_data(price=message.text)
        await state.set_state(AddProduct.quantity)
        await message.answer('Neshta ekanini kiriting:')


@main_router.message(AddProduct.quantity)
async def add_product(message: Message, state: FSMContext):
    if str(message.from_user.id) == ADMIN:
        await state.update_data(quantity=message.text)
        await state.set_state(AddProduct.image)
        await message.answer('Image kiriting:')


@main_router.message(AddProduct.image)
async def add_product(message: Message, state: FSMContext):
    if str(message.from_user.id) == ADMIN:
        img = message.photo[0].file_id
        await state.update_data(image=img)
        await state.set_state(AddProduct.category)
        await message.answer('Category kiriting:')


@main_router.message(AddProduct.category)
async def add_product(message: Message, state: FSMContext):
    if str(message.from_user.id) == ADMIN:
        await state.update_data(category=message.text)
        data = await state.get_data()
        await state.clear()
        text = f""" Everything correct?
                Product id: {data.get('id')}
                Product title: {data.get('title')}
                Product text: {data.get('text')}
                Product price: {data.get('price')}
                Product quantity: {data.get('quantity')}
                Product image: {data.get('image')}
                Category id: {data.get('category')}"""
        await book_scheme(data)
        await message.answer(text)
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


@main_router.message(F.text == '📚 Kitoblar')
async def show_categories(message: Message):
    ikb = InlineKeyboardBuilder()
    for category in category_db.keys():
        ikb.row(InlineKeyboardButton(text=category, callback_data=category))
    ikb.row(InlineKeyboardButton(text='ortga', callback_data='ortga'))
    ikb.adjust(2, repeat=True)
    await message.answer('Tanlang...', reply_markup=ikb.as_markup(resize_keyboard=True))


@main_router.message(F.text == 'Category larni korish')
async def show_categories(message: Message):
    ikb = InlineKeyboardBuilder()
    for category in category_db.keys():
        ikb.row(InlineKeyboardButton(text=category, callback_data=category))
    ikb.row(InlineKeyboardButton(text='ortga', callback_data='ortga'))
    ikb.adjust(2, repeat=True)
    await message.answer('Tanlang...', reply_markup=ikb.as_markup(resize_keyboard=True))


@main_router.message(F.text.in_(category_db))
async def pocc(message: Message):
    ikb = InlineKeyboardBuilder()
    for product in product_db:
        if product_db[product]['category'] == message.text:
            ikb.row(InlineKeyboardButton(text=product_db[product]['title'],
                                         callback_data=product_db[product]['title']))
    ikb.row(InlineKeyboardButton(text='❌', callback_data='delete'),
            InlineKeyboardButton(text='Search 🔍', callback_data='search'))
    ikb.adjust(2, repeat=True)
    await message.answer(f"products of {message.text} category.", reply_markup=ikb.as_markup())


@main_router.callback_query(F.data == 'delete')
async def delete(callback: CallbackQuery, bot: Bot):
    if str(callback.message.from_user.id) == ADMIN:
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        await callback.message.answer('Tanlang...', reply_markup=kb.admin_panel_keyboard)
    else:
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        await callback.message.answer('Tanlang...', reply_markup=kb.user_panel_keyboard)


@main_router.callback_query(F.data == 'ortga')
async def ortga(callback: CallbackQuery, bot: Bot):
    if str(callback.message.from_user.id) == ADMIN:
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        await callback.message.answer('Menu larimizdan birini tanlang...', reply_markup=kb.admin_panel_keyboard)
    else:
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        await callback.message.answer('Menu larimizdan birini tanlang...', reply_markup=kb.user_panel_keyboard)


@main_router.message(F.photo)
async def photo(message: Message):
    await message.answer(message.text)
