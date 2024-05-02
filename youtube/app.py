import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

bot = Bot(token='6832065520:AAHl2kRr7cU8rTo3d9z8bfo9-2w4d-LVGLc')

dp = Dispatcher()


@dp.message(CommandStart())
async def start_cmd(message: types.Message) -> None:
    await message.answer("This is command start")


@dp.message()
async def echo(message: types.Message) -> None:
    text: str | None = message.text

    if text in ["hi", "hello", "hey", "hi there", "hello there"]:
        await message.answer(text)
    elif text in ["bye", "bye bye", "good night"]:
        await message.answer(text)
    else:
        await message.answer(message.text)


async def main() -> None:
    await dp.start_polling(bot)


asyncio.run(main())
