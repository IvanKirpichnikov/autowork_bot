from aiogram import F, Router
from aiogram.types import CallbackQuery
from fluentogram import TranslatorRunner

from src.core.dto import UpdateUserDTO
from src.core.enums import StageType
from src.infrastructure.postgres import DAO
from src.tgbot.keyboards.callback_data import MoreCD
from src.tgbot.keyboards.inline import sign_up
from src.utils import get_datetime


router = Router()


@router.callback_query(MoreCD.filter(F.video == 2))
async def more_to_second_video(
    callback: CallbackQuery,
    l10n: TranslatorRunner,
    dao: DAO
):
    await callback.message.edit_reply_markup(None)
    await callback.message.answer(
        l10n.user.video.second(),
        reply_markup=sign_up(l10n)
    )
    await dao.user.update(
        UpdateUserDTO(
            tid=callback.from_user.id,
            stage=StageType.FIVE.id,
            datetime=get_datetime(StageType.FOUR.delay)
        )
    )
    await callback.answer()


@router.callback_query(MoreCD.filter(F.video == 3))
async def more_to_three_video(
    callback: CallbackQuery,
    l10n: TranslatorRunner,
    dao: DAO
) -> None:
    await callback.message.edit_reply_markup(None)
    await callback.message.answer(
        l10n.url.three(),
        reply_markup=sign_up(l10n)
    )
    await dao.user.update(
        UpdateUserDTO(
            tid=callback.from_user.id,
            stage=StageType.SEVEN.id,
            datetime=get_datetime(StageType.SIX.delay)
        )
    )
    await callback.answer()
