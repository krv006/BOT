from redis_dict import RedisDict

category_db = RedisDict('category_db')
product_db = RedisDict('product_db')

print(product_db)
