from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from fluentogram import TranslatorRunner

from src.core.dto import AddUserDTO, UpdateUserDTO
from src.core.enums import StageType
from src.infrastructure.postgres import DAO
from src.tgbot.filters import CheckSub
from src.tgbot.keyboards.inline import get_access, sign_up
from src.utils import get_datetime


router = Router()
router.message.filter(CommandStart())


@router.message(~CheckSub())
async def user_not_sub_channel(
    message: Message,
    l10n: TranslatorRunner,
    dao: DAO
) -> None:
    await message.answer(
        l10n.user.start(
            full_name=message.from_user.full_name
        )
    )
    await message.answer(
        l10n.user.access(),
        reply_markup=get_access(l10n)
    )
    await dao.user.update(
        UpdateUserDTO(
            tid=message.from_user.id,
            stage=StageType.ONE.id,
            datetime=get_datetime(StageType.ONE.delay)
        )
    )


@router.message(CheckSub())
async def user_sub_channel(
    message: Message,
    l10n: TranslatorRunner,
    dao: DAO
) -> None:
    await message.answer(
        l10n.user.start(
            full_name=message.from_user.full_name
        )
    )
    await message.answer(
        l10n.url.first(),
        reply_markup=sign_up(l10n)
    )
    await dao.user.update(
        UpdateUserDTO(
            tid=message.from_user.id,
            stage=StageType.THREE.id,
            datetime=get_datetime(StageType.TWO.delay)
        )
    )
