import os

from dotenv import load_dotenv
from redis_dict import RedisDict

load_dotenv('../.env')

TOKEN = os.getenv('USTOZ_SHOGIRT')
ADMIN = os.getenv('ADMIN')

category_db = RedisDict('category_db')
product_db = RedisDict('product_db')

