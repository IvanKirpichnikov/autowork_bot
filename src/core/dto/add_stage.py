from dataclasses import dataclass


@dataclass(frozen=True)
class AddStageDTO:
    stage: str
    id: int
