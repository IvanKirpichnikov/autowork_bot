from asyncio import sleep
from typing import AsyncGenerator

from asyncpg import Pool
from taskiq import TaskiqState, TaskiqDepends

from src.core.interfaces.dao import AbstractDAO
from src.infrastructure.postgres.dao import UserDAO


ReturnCreateDAO = AsyncGenerator[AbstractDAO, None]


async def create_user_dao(state: TaskiqState = TaskiqDepends()) -> ReturnCreateDAO:
    pool: Pool = state.pool
    
    await sleep(0.05)
    async with pool.acquire() as connect:
        yield UserDAO(connect)
    await sleep(0.05)
