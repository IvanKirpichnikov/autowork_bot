from json import loads

from aiogram import Bot
from aiogram.filters import BaseFilter
from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from redis.asyncio import Redis


class CheckStatus(BaseFilter):
    async def __call__(
        self,
        event: Message,
        bot: Bot,
        redis: Redis
    ) -> bool:
        sub_chat_id = loads(await redis.get('sub_chat_id'))
        user_id = event.from_user.id
        
        try:
            chat_member = await bot.get_chat_member(
                chat_id=sub_chat_id,
                user_id=user_id
            )
        except TelegramBadRequest:
            return False
        return chat_member.status == ChatMemberStatus.LEFT
