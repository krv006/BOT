from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, \
    CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

import keyboards as kb
from config import ADMIN, book_scheme, category_db, product_db

main_router = Router()


# def make_plus_minus(quantity, product_id):
def make_plus_minus(quantity):
    ikb = InlineKeyboardBuilder()
    ikb.row(InlineKeyboardButton(text="➖", callback_data="change-"),
            InlineKeyboardButton(text=str(quantity), callback_data="number"),
            InlineKeyboardButton(text="➕", callback_data="change+")
            )
    ikb.row(InlineKeyboardButton(text="◀️Orqaga", callback_data="ortga"),
            InlineKeyboardButton(text='🛒 Savatga qo\'shish', callback_data="savatga" + str(quantity)))
    return ikb


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
        await message.answer('Category tanlang:')


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
                Category name: {data.get('category')}"""
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
        ikb.row(InlineKeyboardButton(text=category, callback_data=category + '-cat'))
    ikb.row(InlineKeyboardButton(text='◀️Orqaga', callback_data='ortga'))
    ikb.adjust(2, repeat=True)
    await message.answer('Tanlang...', reply_markup=ikb.as_markup(resize_keyboard=True))


@main_router.callback_query(F.data.endswith('cat'))
async def faa(callback: CallbackQuery, bot: Bot):
    ikb = InlineKeyboardBuilder()
    category_id = callback.data.split('-')[0]
    products_in_category = [product for product, v in product_db.items() if v['category'] == category_id]
    for product_id in products_in_category:
        product = product_db[product_id]
        ikb.row(InlineKeyboardButton(text=product['title'], callback_data=product_id + '-aa'))
    ikb.row(InlineKeyboardButton(text='◀️Orqaga', callback_data='ortga'))
    ikb.adjust(2, repeat=True)
    await bot.edit_message_text(text='Siz tanlagan Categoryni productlari', chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                reply_markup=ikb.as_markup(resize_keyboard=True))


quantity = 1


@main_router.callback_query(F.data.startswith("change"))
async def change_plus(callback: CallbackQuery):
    global quantity
    if callback.data.startswith("change+"):
        quantity += 1
    elif quantity < 2:
        await callback.answer('Eng kamida 1 ta kitob buyurtma qilishingiz mumkin! 😊', show_alert=True)
        return
    else:
        quantity -= 1
    ikb = make_plus_minus(quantity)
    await callback.message.edit_reply_markup(str(callback.message.message_id), reply_markup=ikb.as_markup())


@main_router.callback_query(F.data.endswith('aa'))
async def f(callback: CallbackQuery):
    product_id = callback.data.split('-')[0]
    product = product_db[product_id]
    await callback.message.delete()
    await callback.message.answer(text='Siz tanlagan Kitob haqida malumot')
    ikb = InlineKeyboardBuilder()
    ikb.row(InlineKeyboardButton(text='◀️Orqaga', callback_data='ortga'))
    ikb = make_plus_minus(quantity)
    await callback.message.answer_photo(photo=product['image'],
                                        caption=f"🔹Kitob nomi: {product['title']} \n🔹Kitob haqida:\n{product['text']} \nNarxi💸 : {product['price']}",
                                        reply_markup=ikb.as_markup(resize_keyboard=True))


@main_router.message(F.text == 'Category larni korish')
async def show_categories(message: Message):
    ikb = InlineKeyboardBuilder()
    for category in category_db.keys():
        ikb.row(InlineKeyboardButton(text=category, callback_data=category))
    ikb.row(InlineKeyboardButton(text='◀️Orqaga', callback_data='ortga'))
    ikb.adjust(2, repeat=True)
    await message.answer('Tanlang...', reply_markup=ikb.as_markup(resize_keyboard=True))


# ikb.row(InlineKeyboardButton(text='Search 🔍', callback_data='search'))


@main_router.callback_query(F.data == 'ortga')
async def ortga(callback: CallbackQuery):
    if str(callback.from_user.id) == ADMIN:
        await callback.answer('Siz adminsiz!')
        await callback.answer('Tanlang', reply_markup=kb.admin_panel_keyboard)
    else:
        await callback.answer('Hello user')
        await callback.answer('Tanlang', reply_markup=kb.user_panel_keyboard)
