from asyncpg import Connection

from src.infrastructure.database.db.data import DataDB
from src.infrastructure.database.db.stage import StageDB


async def creating(connect: Connection) -> None:
    await StageDB().create_table(connect)
    await DataDB().create_table(connect)
