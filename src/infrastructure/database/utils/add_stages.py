from asyncpg import Connection

from src.infrastructure.database.db.stage import StageDB
from src.enums.stages import Stages


async def add(connect: Connection) -> None:
    stage_db = StageDB()
    
    for stage in Stages:
        await stage_db.add_data(connect, stage=stage.value)
