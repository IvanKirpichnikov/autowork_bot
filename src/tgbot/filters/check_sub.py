from aiogram import Bot
from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import BaseFilter
from aiogram.types import Message


class CheckSub(BaseFilter):
    async def __call__(
        self,
        event: Message,
        bot: Bot,
        sub_chat_id: int
    ) -> bool:
        try:
            chat_member = await bot.get_chat_member(
                chat_id=sub_chat_id,
                user_id=event.from_user.id
            )
        except TelegramBadRequest:
            return False
        return chat_member.status != ChatMemberStatus.LEFT
