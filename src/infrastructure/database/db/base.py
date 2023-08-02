from abc import ABC, abstractmethod

from asyncpg import Connection


class BaseDB(ABC):
    @abstractmethod
    async def create_table(self, connect: Connection) -> None:
        pass
