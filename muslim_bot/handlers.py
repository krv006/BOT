from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

import keyboards as kb
from config import ADMIN, category_db

main_router = Router()


@main_router.message(CommandStart())
async def start(message: Message):
    if str(message.from_user.id) == ADMIN:
        await message.answer('Siz adminsiz!')
        await message.answer('Tanlang', reply_markup=kb.admin_panel_keyboard)
    else:
        await message.answer('Hello user')
        await message.answer('Tanlang', reply_markup=kb.user_panel_keyboard)
