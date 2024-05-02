from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

import keyboards as kb
from config import ADMIN, userdb, user_schame

main_router = Router()


@main_router.message(F.text == 'Nomoz vaqtini korish')
async def time(message: Message):
    if message.from_user.id != ADMIN:
        await message.answer("Nomoz vaqti : ")
    else:
        await message.answer("Siz adminsiz")

@main_router.message(F.text == 'Qazo nomozlar')
async def qazo(message: Message):
    if message.from_user.id != ADMIN:
        await message.answer("Nomoz vaqti : ")
    else:
        await message.answer("Siz adminsiz")

@main_router.message(F.text == 'Manzilingizdi kiriting')
async def manzil(message: Message):
    if message.from_user.id != ADMIN:
        await message.answer("Nomoz vaqti : ")
    else:
        await message.answer("Siz adminsiz")


# @main_router.message(F.text == 'Nomoz vaqtini korish')
# async def user(message: Message):
#     if str(message.from_user.id) != ADMIN:
#         if AddUser.manzil not in userdb:
#             await message.answer("Register bolmagansiz xali ")
#
#
# @main_router.message(F.text == 'Qazo nomozlar')
# async def user(message: Message):
#     if str(message.from_user.id) != ADMIN:
#         if AddUser.manzil not in userdb:
#             await message.answer("Register bolmagansiz xali ")
#
#
# @main_router.message(F.text == 'Manzilingizdi kiriting')
# async def user(message: Message):
#     if str(message.from_user.id) != ADMIN:
#         if AddUser.manzil not in userdb:
#             await message.answer("Register bolmagansiz xali ")


@main_router.message(CommandStart())
async def start(message: Message):
    if str(message.from_user.id) == ADMIN:
        await message.answer('Siz adminsiz!')
        await message.answer('Tanlang', reply_markup=kb.admin_panel_keyboard)
    else:
        await message.answer(f'Assalomu alaykum {message.from_user.full_name}')
        await message.answer('Tanlang', reply_markup=kb.user_panel_keyboard)


class AddUser(StatesGroup):
    ism = State()
    familya = State()
    manzil = State()


@main_router.message(F.text == "Registratsiya")
async def register(message: Message, state: FSMContext):
    if str(message.from_user.id) != ADMIN:
        await state.set_state(AddUser.ism)
        await message.answer('Ismingizni kiriting: ')


@main_router.message(AddUser.ism)
async def register(message: Message, state: FSMContext):
    if str(message.from_user.id) != ADMIN:
        await state.update_data(ism=message.text)
        await state.set_state(AddUser.familya)
        await message.answer("Familyangizni kiriting: ")


@main_router.message(AddUser.familya)
async def register(message: Message, state: FSMContext):
    if str(message.from_user.id) != ADMIN:
        await state.update_data(familya=message.text)
        await state.set_state(AddUser.manzil)
        await message.answer("Manzilingizni kiriting: ")


@main_router.message(AddUser.manzil)
async def register(message: Message, state: FSMContext):
    if str(message.from_user.id) != ADMIN:
        await state.update_data(familya=message.text)
        data = await state.get_data()
        await state.clear()
        text = f""" Hammasi to'rimi tekshiring: 
                User ism: {data.get('ism')} 
                User familya: {data.get('familya')} 
                User manzil: {data.get('manzil')} 
        """
        await user_schame(data)
        await message.answer(text)
        await message.answer('Saqlandi')


@main_router.message(F.text == 'ortga')
async def ortga(message: Message):
    if str(message.from_user.id) != ADMIN:
        await message.answer(reply_markup=kb.user_panel_keyboard)
    else:
        await message.answer(reply_markup=kb.admin_panel_keyboard)
