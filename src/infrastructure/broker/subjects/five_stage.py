from aiogram import Bot
from aiogram.types import FSInputFile
from fluentogram import TranslatorRunner
from propan import Context, Depends, NatsRouter

from src.core.dto import UpdateUserDTO, UserPubDTO
from src.core.enums import StageType
from src.infrastructure.broker.my_depends import depends
from src.infrastructure.postgres.dao import UserDAO
from src.tgbot.keyboards import inline
from src.utils import get_datetime


router = NatsRouter(prefix='autowork.bot.')


@router.handle('five.stage')
async def send_five_stage(
    message: UserPubDTO,
    dao: UserDAO = Depends(depends),
    bot: Bot = Context('bot'),
    l10n: TranslatorRunner = Context('l10n')
) -> None:
    await bot.send_message(
        message.cid,
        l10n.user.video.second.comment(),
    )
    await bot.send_photo(
        chat_id=message.cid,
        photo=FSInputFile('resources/pictures/poll.png'),
        caption=l10n.user.poll(),
        reply_markup=inline.poll()
    )
    await dao.update(
        UpdateUserDTO(
            tid=message.tid,
            stage=StageType.SIX.id,
            datetime=get_datetime(StageType.FIVE.delay)
        )
    )
