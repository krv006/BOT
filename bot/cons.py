import os

from dotenv import load_dotenv
from redis_dict import RedisDict

load_dotenv('../.env')
TOKEN = os.getenv("TOKEN")
ADMIN_LIST = [1305675046, ]

database = RedisDict('books')
