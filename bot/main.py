import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from cons import TOKEN, database
from routers import start_routers

bot = Bot(TOKEN)


async def on_startup(dispatcher: Dispatcher):
    if not (database.get('categories')):
        database['categories'] = {}
    if not database.get('products'):
        database['products'] = {}
    command_list = [
        BotCommand(command='start', description='Botni boshlash'),
        BotCommand(command='help', description='Yordam'),
    ]
    await bot.set_my_commands(command_list)


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    await bot.delete_my_commands()


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.include_routers(start_routers)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
