from aiogram import F, Router
from aiogram.types import CallbackQuery, FSInputFile
from fluentogram import TranslatorRunner

from src.core.dto import UpdateUserDTO
from src.core.enums import StageType
from src.infrastructure.postgres import DAO
from src.tgbot.keyboards.inline import more_and_sign_up, poll
from src.utils import get_datetime


router = Router(name=__name__)


@router.callback_query(F.data == 'shcijjd3')
async def right_answer(
    callback: CallbackQuery,
    l10n: TranslatorRunner,
    dao: DAO
) -> None:
    await callback.message.edit_reply_markup(None)
    await callback.message.answer(
        l10n.user.poll.true(),
        reply_markup=more_and_sign_up(
            l10n,
            3,
            l10n.inline.three.video()
        )
    )
    await dao.user.update(
        UpdateUserDTO(
            tid=callback.from_user.id,
            stage=StageType.SIX.id,
            datetime=get_datetime(StageType.FIVE.delay)
        )
    )
    await callback.answer()


@router.callback_query(F.data.startswith('shcijjd'))
async def wrong_answer(
    callback: CallbackQuery,
    l10n: TranslatorRunner
) -> None:
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=FSInputFile('resources/pictures/wrong_answer.png'),
        caption=l10n.user.poll.false()
    )
    await callback.message.answer_photo(
        photo=FSInputFile('resources/pictures/poll.png'),
        caption=l10n.user.poll(),
        reply_markup=poll()
    )
    await callback.answer()
