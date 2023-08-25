from dataclasses import dataclass
from datetime import datetime as dt


@dataclass(frozen=True)
class UserDTO:
    id: int
    tid: int
    cid: int
    stage: int
    datetime: dt
