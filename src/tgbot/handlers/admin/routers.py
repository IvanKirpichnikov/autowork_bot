from aiogram import Router

from src.tgbot.handlers.admin import set_channel, sign_up


router = Router(name='admin/router')
files = (set_channel, sign_up)

for file in files:
    router.include_router(file.router)
