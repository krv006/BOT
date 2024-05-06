from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, \
    CallbackQuery, InlineQuery, InlineQueryResultArticle, InputTextMessageContent, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

# import keyboards as kb
from config import ADMIN

main_router = Router()


@main_router.message(CommandStart())
async def start(message: Message):
    rkb = ReplyKeyboardBuilder()
    rkb.row(KeyboardButton(text='Ish joyi kerak'))
    await message.answer(
        f'Assalomu alaykum {message.from_user.first_name} \nUstozShogird kanalining rasmiy botiga xush kelibsiz!',
        reply_markup=rkb.as_markup(resize_keyboard=True))


class AddProduct(StatesGroup):
    name = State()
    age = State()
    texnology = State()
    phone_number = State()
    location = State()
    price = State()
    job = State()
    time = State()
    goal = State()


@main_router.message(F.text == 'Ish joyi kerak')
async def work(message: Message):
    await message.answer(
        "<b>Ish joyi topish uchun ariza berish</b> \nHozir sizga birnecha savollar beriladi. Har biriga javob bering. Oxirida agar hammasi to`g`ri bo`lsa, HA tugmasini bosing va arizangiz Adminga yuboriladi. ")
    await message.answer("<b>Ism, familiyangizni kiriting?</b>")
