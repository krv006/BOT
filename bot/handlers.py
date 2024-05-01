

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from config import ADMIN
import keyboards as kb

main_router = Router()


@main_router.message(CommandStart())
async def welcome(message: Message):
    if str(message.from_user.id) == ADMIN:
        await message.answer("ADMIN")
        await message.answer("Tanlang: ", reply_markup=kb.admin_panel_keyboard)
    else:
        await message.answer("Welcome to!")
        await message.answer("Tanlang: ", reply_markup=kb.user_panel_keyboard)


class AddProduct(FSMContext):
    id = State()
    title = State()
    discription = State()
    price = State()
    brand = State()
    category = State()
    thumbnail = State()
    quantity = State()


@main_router.message(F.text == 'add product')
async def add_product(message: Message, state: FSMContext):
    if str(message.from_user.id) == ADMIN:
        await state.set_state(AddProduct.id)
        await message.answer('ID kiriting: ')
    else:
        ...


@main_router.message(AddProduct.id)
async def add_product(message: Message, state: FSMContext):
    if str(message.from_user.id) == ADMIN:
        await state.update_data(id=message.text)
        await state.set_state(AddProduct.title)
        await message.answer('ID kiriting: ')
    else:
        ...


@main_router.message(AddProduct.title)
async def add_product(message: Message, state: FSMContext):
    if str(message.from_user.id) == ADMIN:
        await state.update_data(title=message.text)
        await state.set_state(AddProduct.discription)
        await message.answer('ID kiriting: ')
    else:
        ...


@main_router.message(AddProduct.discription)
async def add_product(message: Message, state: FSMContext):
    if str(message.from_user.id) == ADMIN:
        await state.update_data(discription=message.text)
        await state.set_state(AddProduct.price)
        await message.answer('Discription kiriting: ')
    else:
        ...


@main_router.message(AddProduct.price)
async def add_product(message: Message, state: FSMContext):
    if str(message.from_user.id) == ADMIN:
        await state.update_data(price=message.text)
        await state.set_state(AddProduct.brand)
        await message.answer('Price kiriting: ')
    else:
        ...


@main_router.message(AddProduct.category)
async def add_product(message: Message, state: FSMContext):
    if str(message.from_user.id) == ADMIN:
        await state.update_data(category=message.text)
        await state.set_state(AddProduct.thumbnail)
        await message.answer('Category kiriting: ')
    else:
        ...


@main_router.message(AddProduct.thumbnail)
async def add_product(message: Message, state: FSMContext):
    if str(message.from_user.id) == ADMIN:
        await state.update_data(thumbnail=message.text)
        await state.set_state(AddProduct.quantity)
        await message.answer('Thumbnail kiriting(rasm): ')
    else:
        ...


@main_router.message(AddProduct.quantity)
async def add_product(message: Message, state: FSMContext):
    if str(message.from_user.id) == ADMIN:
        await state.update_data(quantity=message.text)
        data = await state.get_data()
        await state.clear()
        text = f"""
        id:{data.get('id')}
        """
        await message.answer('Thumbnail kiriting(rasm): ')
    else:
        ...
