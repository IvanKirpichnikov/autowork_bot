from logging import getLogger
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message
from orjson import loads
from redis.asyncio.client import Redis

from src.core.exceptions import ChatGroupIDNotFoundForLogs, ChatGroupIDNotFoundForSub


logger = getLogger('transfer.middleware')


class TransferDataOuterMiddleware(BaseMiddleware):
    def __init__(self, redis: Redis) -> None:
        self._redis = redis
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        sub_chat_id = await self._redis.get('sub_chat_id')
        log_chat_id = await self._redis.get('log_chat_id')
        
        if sub_chat_id is None:
            logger.exception(ChatGroupIDNotFoundForSub)
        
        if log_chat_id is None:
            logger.exception(ChatGroupIDNotFoundForLogs)
        
        data['sub_chat_id'] = loads(sub_chat_id)
        data['log_chat_id'] = loads(log_chat_id)
        
        return await handler(event, data)
