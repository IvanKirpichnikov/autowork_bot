from typing import Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message
from asyncpg import Pool

class CreateConnectMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[dict[str, any]], Awaitable[any]],
        event: Message,
        data: dict[str, any]
    ):
        pool: Pool = data.get('pool')
        async with pool.acquire() as connect:
            data['connect'] = connect
            return await handler(event, data)
