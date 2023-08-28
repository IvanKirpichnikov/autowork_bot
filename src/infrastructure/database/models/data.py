from datetime import datetime

from src.infrastructure.database.models.base import BaseModel


class DataModel(BaseModel):
    tid: int
    cid: int
    stage: int
    datetime: datetime


class NewDataModel(BaseModel):
    id: int
    tid: int
    cid: int
    stage: int
    datetime: datetime
