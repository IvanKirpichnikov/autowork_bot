from dataclasses import dataclass


@dataclass(frozen=True)
class StageDTO:
    stage: str
    id: int
