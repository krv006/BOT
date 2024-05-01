from bot.handlers import main_router
from aiogram import Router

star_router = Router()


start_router = Router()

start_router.include_routers(
    main_router,

)
