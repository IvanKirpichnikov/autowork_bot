from dataclasses import dataclass

from adaptix import Retort


@dataclass(frozen=True)
class UserPubDTO:
    tid: int
    cid: int


user_pub_retort = Retort()
