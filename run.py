import asyncio
import logging

import asyncpg
from redis.asyncio import Redis

from config import Config
from src.bot import main
from src.infrastructure.database.utils import add_stages
from src.infrastructure.database.utils import creating_tables


async def start() -> None:
    config = Config()
    redis = config.redis
    psql = config.psql
    
    pool = await asyncpg.create_pool(
        host=psql.host,
        port=psql.port,
        user=psql.user,
        password=psql.password.get_secret_value(),
        database=psql.database
    )
    redis = Redis(
        host=redis.host,
        port=redis.port,
        password=redis.password.get_secret_value(),
        db=redis.db
    )
    try:
        async with pool.acquire() as connect:
            await creating_tables.creating(connect)
            await add_stages.add(connect)
        await main.start_bot(pool, redis, config)
    finally:
        await redis.close()
        await pool.close()


logging.basicConfig(level=logging.DEBUG)
asyncio.run(start())
