from datetime import datetime as dt
from typing import Optional

from asyncpg import Connection

from src.infrastructure.database.db.base import BaseDB
from src.infrastructure.database.models.data import DataModel


class DataDB(BaseDB):
    async def create_table(self, connect: Connection) -> None:
        async with connect.transaction():
            await connect.execute('''
                CREATE TABLE IF NOT EXISTS data(
                    tid BIGINT UNIQUE,
                    cid BIGINT,
                    stage SMALLINT REFERENCES stages(id),
                    datetime TIMESTAMP(0),
                    PRIMARY KEY(tid, cid)
                )
            ''')
    
    async def add_data(
        self,
        connect: Connection,
        *,
        tid: int,
        cid: int,
        stage: str,
        datetime: dt
    ) -> None:
        async with connect.transaction():
            await connect.execute('''
                INSERT INTO data(
                    tid,
                    cid,
                    stage,
                    datetime
                ) VALUES($1,$2,$3,$4)
                ON CONFLICT (tid) DO UPDATE
                SET stage = $3, datetime = $4
            ''', tid, cid, stage, datetime
            )
    
    async def delete_data(
        self,
        connect: Connection,
        *,
        tid: int
    ) -> None:
        async with connect.transaction():
            await connect.execute('''
                DELETE FROM data WHERE tid = $1
            ''', tid
            )
    
    async def get_data_to_tid(
        self,
        connect: Connection,
        *,
        tid: int
    ) -> DataModel:
        async with connect.transaction():
            data = await connect.fetchrow('''
                SELECT tid,
                       cid,
                       stage,
                       datetime
                FROM data
                WHERE tid = $1
            ''', tid
            )
            return DataModel(**data)
    
    async def get_data(self,connect: Connection) -> Optional[list[DataModel]]:
        async with connect.transaction():
            data = await connect.fetch('''
                SELECT * FROM data
                WHERE datetime::TIMESTAMP(0)
                < now()::TIMESTAMP(0);
            ''')
            
            if not data:
                return None
            
            return [DataModel(**_) for _ in data]
    
    async def update_data(
        self,
        connect: Connection,
        *,
        tid: int,
        stage: int,
        datetime: dt
    ) -> None:
        async with connect.transaction():
            await connect.execute('''
                UPDATE data
                SET stage = $1,
                    datetime = $2
                WHERE tid = $3
            ''', stage, datetime, tid
            )
