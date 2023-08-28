from aiogram import Router

from src.bot.handlers.admin import set_stage, sign_up, set_channel, pagination


router = Router()
files = (pagination, set_stage, set_channel, sign_up)

for file in files:
    router.include_router(file.router)
