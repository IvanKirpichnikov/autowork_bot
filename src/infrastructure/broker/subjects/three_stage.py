from aiogram import Bot
from aiogram.types import FSInputFile
from fluentogram import TranslatorRunner
from propan import Context, Depends, NatsRouter, ContextRepo, NoCast

from src.core.dto import UpdateUserDTO, UserPubDTO
from src.core.enums import StageType
from src.infrastructure.broker.my_depends import depends
from src.infrastructure.postgres.dao import UserDAO
from src.tgbot.keyboards import inline
from src.utils import get_datetime


router = NatsRouter(prefix='autowork.bot.')


@router.handle('three.stage', retry=True)
async def send_three_stage(
g    message: NoCast[UserPubDTO],
    context: ContextRepo,
    dao: NoCast[UserDAO] = Depends(depends)
) -> None:
    bot: Bot = context.get('bot')
    l10n: TranslatorRunner = context.get('l10n')
    await bot.send_photo(
        chat_id=message.cid,
        photo=FSInputFile('resources/pictures/funnel.png'),
        caption=l10n.user.video.first.comment(),
        reply_markup=inline.more_and_sign_up(
            l10n=l10n,
            video=2,
            text=l10n.inline.more()
        )
    )
    await dao.update(
        UpdateUserDTO(
            tid=message.tid,
            stage=StageType.FOUR.id,
            datetime=get_datetime(StageType.THREE.delay)
        )
    )
