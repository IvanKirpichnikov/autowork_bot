from abc import abstractmethod

from src.core.dto import AddStageDTO
from src.core.interfaces.dao import AbstractDAO


class StageAbstractDAO(AbstractDAO):
    @abstractmethod
    async def add(self, stage: AddStageDTO) -> None:
        pass
