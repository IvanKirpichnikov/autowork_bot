from aiogram import Bot
from fluentogram import TranslatorRunner
from propan import Context, Depends, NatsRouter

from src.core.dto import UpdateUserDTO, UserPubDTO
from src.core.enums import StageType
from src.infrastructure.broker.my_depends import depends
from src.infrastructure.postgres.dao import UserDAO
from src.utils import get_datetime


router = NatsRouter(prefix='autowork.bot.')


@router.handle('seven.stage')
async def send_seven_stage(
    message: UserPubDTO,
    dao: UserDAO = Depends(depends),
    bot: Bot = Context('bot'),
    l10n: TranslatorRunner = Context('l10n')
) -> None:
    await bot.send_message(
        chat_id=message.cid,
        text=l10n.user.finish()
    )
    await dao.update(
        UpdateUserDTO(
            tid=message.tid,
            stage=StageType.NINE.id,
            datetime=get_datetime(StageType.NINE.delay)
        )
    )
