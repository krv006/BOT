from aiogram import Router
from aiogram.filters import Command

import requests
from aiogram.types import Message

utils_router = Router()


@utils_router.message(Command(commands='png_to_url'))
async def png_to_url(message: Message):
    with open('../pictures/images.jpeg', 'rb') as f:
        response = requests.post('https://telegra.ph/upload', files={'file': f})
        print(response.status_code)
        data = response.json()
        url = "https://telegra.ph" + data[0].get('src').replace(r"\\", '')
    await message.answer(url)
