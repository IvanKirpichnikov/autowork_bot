from datetime import datetime, timedelta

from aiogram import Bot
from aiogram.types import FSInputFile
from aiogram.utils.markdown import hide_link
from asyncpg import Pool
from taskiq import Context, TaskiqDepends, TaskiqState
from fluentogram import TranslatorRunner

from src.bot.keyboards.inline import get_access, sign_up, pool as pool_kb, more_and_sign_up
from src.infrastructure.database.db.data import DataDB
from src.infrastructure.worker.broker import broker


def get_datetime(incr: int=5) -> datetime:
    return datetime.now().replace(microsecond=0, second=0) \
           + timedelta(minutes=incr)

@broker.task
async def answer_two_stage(
    tid: int,
    cid: int,
    context: Context = TaskiqDepends()
) -> None:
    state: TaskiqState = context.state
    bot: Bot = state.bot
    l10n: TranslatorRunner = state.l10n
    pool: Pool = state.pool
    data_db: DataDB = state.data_db
    
    await bot.send_message(
        chat_id=cid,
        text=hide_link(l10n.channel.url()) + l10n.access.gett(),
        reply_markup=get_access(l10n)
    )
    async with pool.acquire() as connect:
        await data_db.update_data(
            connect,
            tid=tid,
            stage=3,
            datetime=get_datetime(5)
        )

@broker.task
async def answer_three_stage(
    tid: int,
    cid: int,
    context: Context = TaskiqDepends()
) -> None:
    state: TaskiqState = context.state
    bot: Bot = state.bot
    l10n: TranslatorRunner = state.l10n
    pool: Pool = state.pool
    data_db: DataDB = state.data_db
    
    await bot.send_message(
        cid,
        l10n.first.url(),
        reply_markup=sign_up(l10n)
    )
    async with pool.acquire() as connect:
        await data_db.update_data(
            connect,
            tid=tid,
            stage=4,
            datetime=get_datetime(7)
        )

@broker.task
async def answer_four_stage(
    tid: int,
    cid: int,
    context: Context = TaskiqDepends()
) -> None:
    state: TaskiqState = context.state
    bot: Bot = state.bot
    l10n: TranslatorRunner = state.l10n
    pool: Pool = state.pool
    data_db: DataDB = state.data_db
    
    await bot.send_photo(
        chat_id=cid,
        photo=FSInputFile('pictures/funnel.png'),
        caption=l10n.first.video.comment(),
        reply_markup=more_and_sign_up(
            l10n, video=2, text=l10n.more()
        )
    )
    async with pool.acquire() as connect:
        await data_db.update_data(
            connect,
            tid=tid,
            stage=5,
            datetime=get_datetime(5)
        )

@broker.task
async def answer_five_stage(
    tid: int,
    cid: int,
    context: Context = TaskiqDepends()
) -> None:
    state: TaskiqState = context.state
    bot: Bot = state.bot
    l10n: TranslatorRunner = state.l10n
    pool: Pool = state.pool
    data_db: DataDB = state.data_db
    
    await bot.send_message(
        cid,
        l10n.second.video(),
        reply_markup=sign_up(l10n)
    )
    async with pool.acquire() as connect:
        await data_db.update_data(
            connect,
            tid=tid,
            stage=6,
            datetime=get_datetime(7)
        )

@broker.task
async def answer_six_stage(
    tid: int,
    cid: int,
    context: Context = TaskiqDepends()
) -> None:
    state: TaskiqState = context.state
    bot: Bot = state.bot
    l10n: TranslatorRunner = state.l10n
    pool: Pool = state.pool
    data_db: DataDB = state.data_db
    
    await bot.send_message(
        cid,
        l10n.second.video.comment(),
    )
    await bot.send_photo(
        chat_id=cid,
        photo=FSInputFile('pictures/pool.png'),
        caption=l10n.pool(),
        reply_markup=pool_kb()
    )
    async with pool.acquire() as connect:
        await data_db.update_data(
            connect,
            tid=tid,
            stage=7,
            datetime=get_datetime(100)
        )

@broker.task
async def answer_eight_stage(
    tid: int,
    cid: int,
    context: Context = TaskiqDepends()
) -> None:
    state: TaskiqState = context.state
    bot: Bot = state.bot
    l10n: TranslatorRunner = state.l10n
    pool: Pool = state.pool
    data_db: DataDB = state.data_db
    
    await bot.send_message(
        cid,
        l10n.third.url(),
        reply_markup=sign_up(l10n)
    )
    async with pool.acquire() as connect:
        await data_db.update_data(
            connect,
            tid=tid,
            stage=9,
            datetime=get_datetime(7)
        )

@broker.task
async def answer_nine_stage(
    tid: int,
    cid: int,
    context: Context = TaskiqDepends()
) -> None:
    state: TaskiqState = context.state
    bot: Bot = state.bot
    l10n: TranslatorRunner = state.l10n
    pool: Pool = state.pool
    data_db: DataDB = state.data_db
    
    await bot.send_message(
        cid,
        l10n.finish(),
        reply_markup=sign_up(l10n)
    )
    async with pool.acquire() as connect:
        await data_db.update_data(
            connect,
            tid=tid,
            stage=1,
            datetime=get_datetime(100)
        )
