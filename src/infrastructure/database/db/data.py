from datetime import datetime as dt
from typing import Optional

from asyncpg import Connection

from src.infrastructure.database.db.base import BaseDB
from src.infrastructure.database.models.data import DataModel, NewDataModel
from src.infrastructure.database.models.user import UserDataModel


class DataDB(BaseDB):
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
            await connect.execute(
                '''
                    INSERT INTO users(
                        tid,
                        cid,
                        stage,
                        datetime
                    ) VALUES($1,$2,$3,$4)
                    ON CONFLICT (tid) DO UPDATE
                    SET stage = $3, datetime = $4
                ''', tid, cid, stage, datetime
            )
    async def get_users(
        self,
        connect: Connection,
        *,
        offset: int
    ) -> Optional[UserDataModel]:
        async with connect.transaction(readonly=True):
            cursor = await connect.cursor(
                '''
                SELECT LAG(id) OVER(ORDER BY id) AS back_id,
                       id AS current_id,
                       LEAD(id) OVER(ORDER BY id) AS next_id
                  FROM users
                 LIMIT 1 OFFSET $1;
                ''', offset
            )
            data = await cursor.fetchrow()
        back_id = data.get('back_id')
        current_id = data.get('current_id')
        next_id = data.get('next_id')
        
        if (back_id, current_id, next_id) == (None, None, None):
            return None
        
        user = await self.get_data_to_id(connect, id=current_id)
        
        return UserDataModel(
            back_id=back_id,
            data=NewDataModel(**vars(user)),
            next_id=next_id
        )
    
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
    ) -> DataModel:
        async with connect.transaction():
            data = await connect.fetchrow(
                '''
                    SELECT id,
                           tid,
                           cid,
                           stage,
                           datetime
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
