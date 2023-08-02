from aiogram import Router

from src.bot.filters.check_sub import CheckSubToChatID
from src.bot.handlers.user import pool, more, start


router = Router()
files = (pool, more)
_ = 0

router.include_router(start.router)

for file in files:
    file.router.message.filter(CheckSubToChatID())
    router.include_router(file.router)
