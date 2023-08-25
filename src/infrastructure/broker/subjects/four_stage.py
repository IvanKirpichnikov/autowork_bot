from aiogram import Bot
from fluentogram import TranslatorRunner
from propan import Context, Depends, NatsRouter

from src.core.dto import UpdateUserDTO, UserPubDTO
from src.core.enums import StageType
from src.infrastructure.broker.my_depends import depends
from src.infrastructure.postgres.dao import UserDAO
from src.tgbot.keyboards import inline
from src.utils import get_datetime


router = NatsRouter(prefix='autowork.bot.')


@router.handle('four.stage')
async def send_four_stage(
    message: UserPubDTO,
    dao: UserDAO = Depends(depends),
    bot: Bot = Context('bot'),
    l10n: TranslatorRunner = Context('l10n')
) -> None:
    await bot.send_message(
        message.cid,
        l10n.user.video.second(),
        reply_markup=inline.sign_up(l10n)
    )
    await dao.update(
        UpdateUserDTO(
            tid=message.tid,
            stage=StageType.FIVE.id,
            datetime=get_datetime(StageType.FOUR.delay)
        )
    )
