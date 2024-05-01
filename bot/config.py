import os

from dotenv import load_dotenv
from pip._internal.resolution.resolvelib import requirements
from redis_dict import RedisDict

load_dotenv('../.env')

TOKEN = os.getenv('TOKEN')
ADMIN = os.getenv('ADMIN')

category_db = RedisDict('category_db')
product_db = RedisDict('product_db')


async def product_scheme(data):
    product_db[data['id']] = data

