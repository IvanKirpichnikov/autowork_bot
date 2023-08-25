from asyncpg import Connection

from src.infrastructure.postgres.dao import StageDAO, UserDAO


class DAO:
    __slots__ = ('user', 'stage')
    
    def __init__(self, connect: Connection) -> None:
        self.user = UserDAO(connect)
        self.stage = StageDAO(connect)
