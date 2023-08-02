from aiogram import Router
from asyncpg import Pool
from redis.asyncio import Redis


from src.bot.handlers.user import routers as u_r
from src.bot.handlers.admin import routers as a_r


router = Router()

router.include_routers(
    a_r.router,
    u_r.router
)


@router.shutdown()
async def close(
    pool: Pool,
    redis: Redis
) -> None:
    await pool.close()
    await redis.close()
