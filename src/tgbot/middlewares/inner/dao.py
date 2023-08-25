from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from asyncpg import Pool

from src.infrastructure.postgres import DAO


class DAOMiddleware(BaseMiddleware):
    def __init__(self, pool: Pool) -> None:
        self._pool = pool
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        async with self._pool.acquire() as connect:
            data['dao'] = DAO(connect)
            await handler(event, data)
