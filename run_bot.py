import asyncio
import logging

import asyncpg
from redis.asyncio import Redis

from src.core.configs import config
from src.infrastructure.broker import app
from src.tgbot import start_bot
from src.infrastructure.postgres.utils import add_stages, creating_tables
from src.utils import create_postgres_pool


async def run() -> None:
    pool = await create_postgres_pool(config)
    redis = Redis(
        host=config.redis.host,
        port=config.redis.port,
        password=config.redis.password,
        db=config.redis.db
    )
    try:
        async with pool.acquire() as connect:
            await creating_tables(connect)
            await add_stages(connect)
        await start_bot(pool, redis, config)
    except Exception as ex:
        raise ex
    finally:
        await pool.close()
        await redis.close()


logging.basicConfig(level=logging.DEBUG)
asyncio.run(run())
