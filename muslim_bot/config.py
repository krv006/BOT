import os

from dotenv import load_dotenv
from redis_dict import RedisDict

load_dotenv('../.env')

TOKEN = os.getenv('TOKEN1')
ADMIN = os.getenv('ADMIN')

userdb = RedisDict('category_db')


async def user_schame(data):
    userdb[data.get('ism')] = {
        'ism': data.get('ism'),
        'familya': data.get('familya'),
        'manzil': data.get('manzil'),
    }


print(userdb)