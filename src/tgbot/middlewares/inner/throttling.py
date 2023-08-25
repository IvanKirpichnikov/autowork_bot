from typing import Any, Awaitable, Callable, Dict, Union

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject
from cachetools import TTLCache


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = 0.7):
        self.cache = TTLCache(maxsize=10000, ttl=rate_limit)
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Union[CallbackQuery, Message],
        data: Dict[str, Any]
    ) -> Any:
        user = data.get('event_from_user')
        
        if user is None:
            return None
        if user.id in self.cache:
            return None
        
        self.cache[user.id] = None
        return await handler(event, data)
