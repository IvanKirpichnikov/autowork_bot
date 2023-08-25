from asyncpg import create_pool, Pool

from src.core.configs import Config


async def create_postgres_pool(config: Config) -> Pool:
    """
    Create asyncpg Pool
    
    :param config: config
    :return: asyncpg.Pool
    """
    
    return await create_pool(
        host=config.psql.host,
        port=config.psql.port,
        user=config.psql.user,
        password=config.psql.password,
        database=config.psql.database
    )
