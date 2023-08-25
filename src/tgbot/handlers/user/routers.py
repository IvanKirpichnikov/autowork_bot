from aiogram import Router

from src.tgbot.filters import CheckSub
from src.tgbot.handlers.user import more, poll, set_stage, start


router = Router(name=__name__)
files = (poll, more, set_stage)
_ = 0

router.include_router(start.router)

for file in files:
    file.router.message.filter(CheckSub())
    router.include_router(file.router)
