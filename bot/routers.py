from aiogram import Router

from handlers import main_router
from pagination import pagination_router
from untils import utils_router

start_router = Router()

start_router.include_routers(
    main_router,
    utils_router,
    pagination_router,
)
