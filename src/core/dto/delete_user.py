from dataclasses import dataclass


@dataclass(frozen=True)
class DeleteUserDTO:
    tid: int
