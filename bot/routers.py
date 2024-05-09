from aiogram import Router

from admin import admin_router
from basket import basket_router
from handlers import main_router
from inline_mode import inline_router
from order import order_router

start_routers = Router()

start_routers.include_routers(
    inline_router,
    admin_router,
    basket_router,
    order_router,
    main_router,
)
