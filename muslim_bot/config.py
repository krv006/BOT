import os

from dotenv import load_dotenv
from redis_dict import RedisDict

load_dotenv('../.env')

TOKEN = os.getenv('TOKEN1')
ADMIN = os.getenv('ADMIN')


category_db = RedisDict('category_db')
