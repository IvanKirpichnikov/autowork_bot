from logging import getLogger

from aiogram import Router
from asyncpg import Pool
from redis.asyncio.client import Redis

from src.tgbot.handlers.admin import routers as a_r
from src.tgbot.handlers.user import routers as u_r


logger = getLogger('autowork.bot')

router = Router()
router.include_routers(
    a_r.router,
    u_r.router
)


@router.shutdown()
async def close(pool: Pool, redis: Redis) -> None:
    await pool.close()
    await redis.close()
    logger.warning('Closed redis connect and postgres pool')
