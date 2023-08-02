from typing import Callable

from src.infrastructure.worker import tasks


def select(stage: int) -> Callable:
    if stage == 2:
        return tasks.answer_two_stage
    if stage == 3:
        return tasks.answer_three_stage
    if stage == 4:
        return tasks.answer_four_stage
    if stage == 5:
        return tasks.answer_five_stage
    if stage == 6:
        return tasks.answer_six_stage
    if stage == 8:
        return tasks.answer_eight_stage
    if stage == 9:
        return tasks.answer_nine_stage
