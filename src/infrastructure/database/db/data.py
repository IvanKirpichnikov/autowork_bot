from datetime import datetime as dt
from typing import List, Optional

from asyncpg import Connection

from src.infrastructure.database.db.base import BaseDB
from src.infrastructure.database.models.data import DataModel, NewDataModel, NewNewDataModel
from src.infrastructure.database.models.user import UserDataModel


class DataDB(BaseDB):
    async def add_data(
        self,
        connect: Connection,
        *,
        tid: int,
        cid: int,
        stage: int,
        datetime: dt,
        username: str
    ) -> None:
        async with connect.transaction():
            await connect.execute(
                '''
                    INSERT INTO users(
                        tid,
                        cid,
                        stage,
                        datetime,
                        registration,
                        username
                    ) VALUES($1,$2,$3,$4, $5::TIMESTAMP(0), $6)
                    ON CONFLICT (tid) DO UPDATE
                    SET stage = $3, datetime = $4, username = $6
                ''', tid, cid, stage, datetime, dt.now(), username or "-"
            )
    async def pagination(
        self,
        connect: Connection,
        *,
        offset: int
    ) -> List[NewNewDataModel]:
        data = await connect.fetch('''
            SELECT id,
                   username,
                   stage,
                   registration
              FROM users
              ORDER BY id;
        ''')
        
        return [NewNewDataModel(**_) for _ in data]
    
    async def delete_data(
        self,
        connect: Connection,
        *,
        tid: int
    ) -> None:
        async with connect.transaction():
            await connect.execute(
                'DELETE FROM users WHERE tid = $1',
                tid
            )
    
    async def get_data_to_tid(
        self,
        connect: Connection,
        *,
        tid: int
    ) -> DataModel:
        async with connect.transaction():
            data = await connect.fetchrow(
                '''
                    SELECT tid,
                           cid,
                           stage,
                           datetime
                    FROM users
                    WHERE tid = $1
                ''', tid
            )
            return DataModel(**data)
    
    async def get_data_to_id(
        self,
        connect: Connection,
        *,
        id: int
    ) -> NewDataModel:
        async with connect.transaction():
            data = await connect.fetchrow(
                '''
                    SELECT id,
                           tid,
                           cid,
                           stage,
                           registration
                    FROM users
                    WHERE id = $1
                ''', id
            )
            return NewDataModel(**data)
    
    async def get_data(self, connect: Connection) -> Optional[list[DataModel]]:
        async with connect.transaction():
            data = await connect.fetch(
                '''
                    SELECT * FROM users
                    WHERE datetime::TIMESTAMP(0)
                    < now()::TIMESTAMP(0);
                '''
            )
            
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
            await connect.execute(
                '''
                    UPDATE users
                    SET stage = $1,
                        datetime = $2
                    WHERE tid = $3
                ''', stage, datetime, tid
            )
