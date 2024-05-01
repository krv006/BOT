import os

from dotenv import load_dotenv
from redis_dict import RedisDict

load_dotenv('../.env')

TOKEN = os.getenv('TOKEN')
ADMIN = os.getenv('ADMIN')

category_db = RedisDict('category_db')
product_db = RedisDict('product_db')


async def product_scheme(data):
    product_db[data.get('id')] = {
        'id': data.get('id'),
        'title': data.get('title'),
        'description': data.get('description'),
        'price': data.get('price'),
        'brand': data.get('brand'),
        'category': data.get('category'),
        'thumbnail': data.get('thumbnail'),
        'quantity': data.get('quantity')

    }

print(product_db)