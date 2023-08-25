from abc import abstractmethod
from typing import List, Optional

from src.core.dto import AddUserDTO, DeleteUserDTO, GetUserByIDDTO, GetUserByStage, UpdateUserDTO, UserDTO
from src.core.interfaces.dao import AbstractDAO


class UserAbstractDAO(AbstractDAO):
    @abstractmethod
    async def add(self, dto: AddUserDTO) -> None:
        pass
    
    @abstractmethod
    async def delete(self, user: DeleteUserDTO) -> None:
        pass
    
    @abstractmethod
    async def get_by_tid(self, dto: GetUserByIDDTO) -> UserDTO:
        pass
    
    @abstractmethod
    async def get_by_stage(self, dto: GetUserByStage) -> Optional[List[UserDTO]]:
        pass
    
    @abstractmethod
    async def update(self, dto: UpdateUserDTO) -> None:
        pass
