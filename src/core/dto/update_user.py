from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class UpdateUserDTO:
    """
    :param tid:
    :param stage:
    :param datetime:
    
    """
    tid: int
    stage: int
    datetime: datetime
