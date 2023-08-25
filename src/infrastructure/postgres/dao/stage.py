from asyncpg import Connection

from src.core.dto import AddStageDTO
from src.core.interfaces.dao import StageAbstractDAO


class StageDAO(StageAbstractDAO):
    __slots__ = ('connect',)
    
    def __init__(self, connect: Connection) -> None:
        self.connect = connect
    
    async def add(self, stage: AddStageDTO) -> None:
        await self.connect.execute(
            '''
            INSERT INTO stages( id, stage)
            VALUES ($1, $2)
            ON CONFLICT DO NOTHING
            ''',
            stage.id, stage.stage
        )
