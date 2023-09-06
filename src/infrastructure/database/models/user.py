from typing import Optional

from src.infrastructure.database.models.base import BaseModel
from src.infrastructure.database.models.data import NewDataModel


class UserDataModel(BaseModel):
    back_id: Optional[int]
    data: NewDataModel
    next_id: Optional[int]
