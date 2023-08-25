from typing import List, Optional

from asyncpg import Connection

from src.core.dto import AddUserDTO, DeleteUserDTO, GetUserByIDDTO, GetUserByStage, UpdateUserDTO, UserDTO
from src.core.interfaces.dao import UserAbstractDAO
from src.core.loggers import dao


class UserDAO(UserAbstractDAO):
    __slots__ = ('connect',)
    
    def __init__(self, connect: Connection) -> None:
        self.connect = connect
    
    async def add(self, dto: AddUserDTO) -> None:
        await self.connect.execute(
            '''
            INSERT INTO users(
                tid, cid, stage, datetime
            )
            VALUES(
                $1, $2, $3, $4
            )
            ON CONFLICT(tid) DO UPDATE
            SET stage = $3, datetime = $4;
            ''',
            dto.tid,
            dto.cid,
            dto.stage,
            dto.datetime
        )
        print(dto.tid)
        dao.warning(
            'Added user. User ID=%d',
            dto.tid
        )
    
    async def delete(self, dto: DeleteUserDTO) -> None:
        await self.connect.execute(
            'DELETE FROM users WHERE tid = $1;',
            dto.tid
        )
        dao.warning(
            'Delete user. User ID=%r',
            dto.tid
        )
    
    async def get_by_tid(self, dto: GetUserByIDDTO) -> UserDTO:
        connect = self.connect
        async with connect.transaction():
            cursor = await connect.cursor(
                '''
                SELECT id, tid, cid, stage, datetime
                  FROM users
                 WHERE tid = $1
                 LIMIT 1;
                ''',
                dto.tid
            )
            data = await cursor.fetchrow()
            dao.info(
                'Get user by user id. User ID=%r',
                dto.tid
            )
            return UserDTO(**data)
    
    async def get_by_stage(self, dto: GetUserByStage) -> Optional[List[UserDTO]]:
        data = await self.connect.fetch(
            '''
            SELECT id,
                   tid,
                   cid,
                   stage,
                   datetime
              FROM users
             WHERE datetime::TIMESTAMP(0) <= NOW()::TIMESTAMP(0)
             AND stage = $1;
            ''',
            dto.stage
        )
        if data:
            dao.info(
                'Get users by stage. Stage=%r. Len=%r',
                dto.stage,
                len(data)
            )
            return [UserDTO(**_) for _ in data]
        dao.info(
            'Get users Get users by stage. Stage=%r. Len=0',
            dto.stage,
        )
    
    async def update(self, dto: UpdateUserDTO) -> None:
        await self.connect.execute(
            '''
            UPDATE users
               SET stage = $1,
                   datetime = $2
             WHERE tid = $3
            ''',
            dto.stage,
            dto.datetime,
            dto.tid
        )
        # dao.warning(
        #     'Update user data. User ID=%d',
        #     dto.tid
        # )
