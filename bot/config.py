import os

from dotenv import load_dotenv
from redis_dict import RedisDict

load_dotenv('../.env')

TOKEN = os.getenv('TOKEN')
ADMIN = os.getenv('ADMIN')

category_db = RedisDict('category_db')
product_db = RedisDict('product_db')


async def book_scheme(data):
    product_db[data.get('id')] = {
        'id': data.get('id'),
        'title': data.get('title'),
        'text': data.get('title'),
        'image': data.get('image'),
        'price': data.get('price'),
        'category': data.get('category')
    }


print(product_db)
print(category_db)

# product_db.clear()
# category_db.clear()
