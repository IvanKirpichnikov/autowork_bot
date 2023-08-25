from dataclasses import dataclass


@dataclass(frozen=True)
class StageMixin:
    stage: str
    id: int
    delay: int
