from asyncpg import Connection


async def _create_users_table(connect: Connection) -> None:
    await connect.execute(
        '''
        CREATE TABLE IF NOT EXISTS users(
            PRIMARY KEY(id),
            id       SERIAL   NOT NULL,
            tid      BIGINT   UNIQUE,
            cid      BIGINT   UNIQUE,
            stage    SMALLINT REFERENCES stages(id),
            datetime TIMESTAMP(0)
        );
        '''
    )


async def _create_stages_table(connect: Connection) -> None:
    await connect.execute(
        '''
        CREATE TABLE IF NOT EXISTS stages(
            id    SMALLINT PRIMARY KEY,
            stage TEXT     UNIQUE
        );
        '''
    )


async def creating_tables(connect: Connection) -> None:
    await _create_stages_table(connect)
    await _create_users_table(connect)
