from asyncpg import Connection

from src.infrastructure.database.db.base import BaseDB


class StageDB(BaseDB):
    async def create_table(self, connect: Connection) -> None:
        async with connect.transaction():
            await connect.execute('''
                CREATE TABLE IF NOT EXISTS stages(
                    id SMALLSERIAL PRIMARY KEY,
                    stage TEXT UNIQUE
                )
            ''')
    
    async def add_data(
        self,
        connect: Connection,
        stage: str
    ) -> None:
        async with connect.transaction():
            await connect.execute('''
                INSERT INTO stages(stage)
                VALUES ($1) ON CONFLICT DO NOTHING
            ''', stage
            )
