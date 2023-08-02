from cachetools import TTLCache
from typing import Awaitable, Callable, Union

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject


class TrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float=2.0):
        self.cache = TTLCache(maxsize=10000, ttl=rate_limit)
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, any]], Awaitable[any]],
        event: Union[CallbackQuery, Message],
        data: dict[str, any]
    ) -> None:
        user = data.get('event_from_user')
        if user is None:
            return
        if user.id in self.cache:
            return
        self.cache[user.id] = None
        return await handler(event, data)
