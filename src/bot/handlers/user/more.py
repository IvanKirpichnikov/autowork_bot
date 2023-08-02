from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.types import CallbackQuery
from asyncpg import Connection
from fluentogram import TranslatorRunner

from src.bot.keyboards.inline import MoreCD, sign_up
from src.infrastructure.database.db.data import DataDB


router = Router()


@router.callback_query(MoreCD.filter(F.video == 2))
async def more_to_second_video(
    callback: CallbackQuery,
    l10n: TranslatorRunner,
    connect: Connection,
    data_db: DataDB
):
    await callback.message.edit_reply_markup(None)
    await callback.message.answer(
        l10n.second.video(),
        reply_markup=sign_up(l10n)
    )
    await data_db.update_data(
        connect,
        tid=callback.from_user.id,
        stage=6,
        datetime=datetime.now().replace(
            microsecond=0, second=0
        ) + timedelta(minutes=7)
    )
    await callback.answer()

@router.callback_query(MoreCD.filter(F.video == 3))
async def more_to_thrid_video(
    callback: CallbackQuery,
    l10n: TranslatorRunner,
    connect: Connection,
    data_db: DataDB
) -> None:
    await callback.message.edit_reply_markup(None)
    await callback.message.answer(
        l10n.third.url(),
        reply_markup=sign_up(l10n)
    )
    await data_db.update_data(
        connect,
        tid=callback.from_user.id,
        stage=7,
        datetime=datetime.now().replace(
            microsecond=0, second=0
        ) + timedelta(minutes=7)
    )
    await callback.answer()
