from datetime import datetime
from datetime import timedelta

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from asyncpg import Connection
from fluentogram import TranslatorRunner

from src.bot.filters.check_status import CheckStatus
from src.bot.keyboards.inline import sign_up, get_access
from src.infrastructure.database.db.data import DataDB


router = Router()


@router.message(CommandStart(), CheckStatus())
async def greetting_not_sub_channel(
    message: Message,
    l10n: TranslatorRunner,
    connect: Connection,
    data_db: DataDB
) -> None:
    await message.answer(
        l10n.start(
            full_name=message.from_user.full_name
        )
    )
    await message.answer(
        l10n.access.gett(),
        reply_markup=get_access(l10n)
    )
    await data_db.add_data(
        connect,
        tid=message.from_user.id,
        cid=message.chat.id,
        stage=3,
        datetime=datetime.now().replace(
            microsecond=0, second=0
        ) + timedelta(minutes=5)
    )

@router.message(CommandStart(), ~CheckStatus())
async def greetting_sub_channel(
    message: Message,
    l10n: TranslatorRunner,
    connect: Connection,
    data_db: DataDB
) -> None:
    await message.answer(
        l10n.start(
            full_name=message.from_user.full_name
        )
    )
    await message.answer(
        l10n.first.url(),
        reply_markup=sign_up(l10n)
    )
    user_id = message.from_user.id
    await data_db.add_data(
        connect,
        tid=user_id,
        cid=message.chat.id,
        stage=2,
        datetime=datetime.now().replace(
            microsecond=0, second=0
        ) + timedelta(minutes=1)
    )
    await data_db.update_data(
        connect,
        tid=user_id,
        stage=4,
        datetime=datetime.now().replace(
            microsecond=0, second=0
        ) + timedelta(minutes=5)
    )
