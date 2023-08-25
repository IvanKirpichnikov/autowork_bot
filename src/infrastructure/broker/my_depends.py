from asyncio import sleep
from typing import AsyncGenerator
from contextlib import asynccontextmanager

from asyncpg import Pool
from propan import ContextRepo

from src.core.dto import UpdateUserDTO, UserPubDTO
from src.core.enums import StageType
from src.core.interfaces.dao import AbstractDAO
from src.infrastructure.postgres.dao import UserDAO
from src.utils import get_datetime


@asynccontextmanager
async def depends(message: UserPubDTO, context: ContextRepo) -> AsyncGenerator[AbstractDAO, None]:
    """
    Create UserDAO and update user stage
    
    :param message: src.core.dto.UserPubDTO
    :param pool: asyncpg.Pool
    :return: AsyncGenerator[AbstractDAO, None, None]
    
    """
    pool: Pool = context.get('pool')
    async with pool.acquire() as connect:
        dao = UserDAO(connect)
        yield dao
        await dao.update(
            UpdateUserDTO(
                tid=message.tid,
                stage=StageType.NINE.id,
                datetime=get_datetime(StageType.NINE.delay)
            )
        )
