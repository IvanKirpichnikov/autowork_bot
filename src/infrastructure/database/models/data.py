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
    registration: datetime

class NewNewDataModel(BaseModel):
    id: int
    username: str
    stage: int
    registration: datetime
