import asyncio
import logging
import os
import sys
from typing import Iterable

from aiogram import BaseMiddleware
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, ChatMemberStatus
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, CallbackQuery
from aiogram.types import Message
from aiogram.types.update import Update
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv
from redis_dict import RedisDict

load_dotenv('.env')
TOKEN = os.getenv("TOKEN")
dp = Dispatcher()

users = RedisDict('users')

CHANNEL_IDS = {
    -1002065914255: {
        'text': '1 - Kanal',
        'url': 'https://t.me/kokookoksd',
    }
}


def make_channels_button(channel_ids: Iterable):
    ikb = InlineKeyboardBuilder()
    for channel_id in channel_ids:
        ikb.row(InlineKeyboardButton(**CHANNEL_IDS[channel_id]))
    ikb.row(InlineKeyboardButton(text='Tasdiqlash', callback_data='confirm'))
    return ikb.as_markup()


class SubscriptionMiddleware(BaseMiddleware):
    async def __call__(self, handler, update: Update, data):
        unsubscribe_channels = []
        for channel_id in CHANNEL_IDS:
            member = await update.bot.get_chat_member(channel_id, update.event.from_user.id)
            if member.status == ChatMemberStatus.LEFT:
                unsubscribe_channels.append(channel_id)
        return unsubscribe_channels

@dp.message(CommandStart())
async def check_messages(message: Message):
    if message.forward_from_chat:
        await message.answer(str(message.forward_from_chat.id).replace('-', ''))
    await message.answer('Xush kelibsiz botga')


@dp.callback_query(F.data.startswith('confirm'))
async def check_messages(callback_query: CallbackQuery, bot: Bot):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await callback_query.answer('Tasdiqlandi')
    users[str(callback_query.from_user.id)] = True


async def main() -> None:
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2))
    dp.update.outer_middleware(SubscriptionMiddleware())
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
