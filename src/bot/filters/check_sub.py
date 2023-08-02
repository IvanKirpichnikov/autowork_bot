import json

from aiogram import Bot
from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import BaseFilter
from aiogram.types import Message
from redis.asyncio import Redis


class CheckSubToChatID(BaseFilter):
    async def __call__(
        self,
        message: Message,
        bot: Bot,
        redis: Redis
    ) -> bool:
        user_id = message.from_user.id
        if user_id is None:
            return False
        
        data = await redis.get('sub_chat_id')
        if data is None:
            raise ValueError('Отсутствует канал для подписывания. Добавьте бота в канал')
        
        chat_id = json.loads(data)
        try:
            result = await bot.get_chat_member(
                chat_id=chat_id,
                user_id=user_id
            )
            return result.status != ChatMemberStatus.LEFT
        except TelegramBadRequest:
            return False
