from datetime import datetime
from datetime import timedelta

from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from asyncpg import Connection
from fluentogram import TranslatorRunner

from src.bot.keyboards.inline import more_and_sign_up, pool as pool_kb
from src.infrastructure.database.db.data import DataDB


router = Router()


@router.callback_query(F.data == 'shcijjd3')
async def right_answer(
    callback: CallbackQuery,
    l10n: TranslatorRunner,
    connect: Connection,
    data_db: DataDB
) -> None:
    await callback.message.edit_reply_markup(None)
    await callback.message.answer(
        l10n.pool.true(),
        reply_markup=more_and_sign_up(
            l10n,
            3,
            l10n.third.video()
        )
    )
    await data_db.update_data(
        connect,
        tid=callback.from_user.id,
        stage=8,
        datetime=datetime.now().replace(
            microsecond=0, second=0
        ) + timedelta(minutes=7)
    )
    await callback.answer()

@router.callback_query(F.data.startswith('shcijjd'))
async def wrong_answer(
    callback: CallbackQuery,
    l10n: TranslatorRunner
) -> None:
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=FSInputFile('pictures/wrong_answer.png'),
        caption=l10n.pool.false()
    )
    await callback.message.answer_photo(
        photo=FSInputFile('pictures/pool.png'),
        caption=l10n.pool(),
        reply_markup=pool_kb()
    )
    await callback.answer()
