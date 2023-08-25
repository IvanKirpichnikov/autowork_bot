import uuid6
from propan import NatsBroker
from taskiq import Context, TaskiqDepends

from src.core.dto import GetUserByStage
from src.core.enums import StageType
from src.infrastructure.postgres.dao import UserDAO
from src.infrastructure.scheduler import create_user_dao
from src.infrastructure.scheduler.app import broker
from src.utils import compress_dict


@broker.task(schedule=[{"cron": "*/1 * * * *"}])
async def send_publish(
    context: Context = TaskiqDepends(),
    dao: UserDAO = TaskiqDepends(create_user_dao)
) -> None:
    nats: NatsBroker = context.state.nats
    users = await dao.get_by_stage(
        GetUserByStage(StageType.THREE.id)
    )
    
    if users is None:
        return None
    
    for user in users:
        await nats.publish(
            message=compress_dict(
                tid=user.tid,
                cid=user.cid
            ),
            subject='autowork.bot.three.stage',
            headers={
                'Nats-Msg-Id': uuid6.uuid8().hex
            }
        )
    return None
