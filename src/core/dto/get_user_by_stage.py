from dataclasses import dataclass


@dataclass(frozen=True)
class GetUserByStage:
    stage: int
