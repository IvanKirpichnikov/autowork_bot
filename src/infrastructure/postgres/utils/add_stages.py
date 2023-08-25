from asyncpg import Connection

from src.core.dto import AddStageDTO
from src.core.enums.stages import StageType
from src.infrastructure.postgres.dao import StageDAO


async def add_stages(connect: Connection) -> None:
    stage = StageDAO(connect)
    
    for stage_type in StageType:
        await stage.add(
            AddStageDTO(
                stage=stage_type.stage,
                id=stage_type.id
            )
        )
