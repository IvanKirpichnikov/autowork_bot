from datetime import datetime
from datetime import timedelta
from json import loads

from aiogram import Bot, Router, F
from aiogram.enums import ChatType
from aiogram.filters import ChatMemberUpdatedFilter, IS_MEMBER, MEMBER, LEFT, KICKED
from aiogram.types import ChatMemberUpdated
from asyncpg import Connection
from fluentogram import TranslatorRunner
from redis.asyncio import Redis

from src.bot.keyboards.inline import sign_up
from src.infrastructure.database.db.data import DataDB


router = Router()
router.my_chat_member()


@router.my_chat_member(
    ChatMemberUpdatedFilter(KICKED>>MEMBER),
    F.chat.type == ChatType.PRIVATE
)
async def add_user(
    event: ChatMemberUpdated,
    connect: Connection,
    data_db: DataDB
):
    date_time = datetime.now().replace(
        microsecond=0, second=0
    ) + timedelta(minutes=5)
    await data_db.update_data(
        connect,
        tid=event.from_user.id,
        stage=2,
        datetime=date_time
    )

@router.my_chat_member(
    ChatMemberUpdatedFilter(MEMBER>>LEFT),
    F.chat.type == ChatType.PRIVATE
)
async def remove_user(
    event: ChatMemberUpdated,
    connect: Connection,
    data_db: DataDB
):
    await data_db.delete_data(
        connect,
        tid=event.from_user.id
    )

@router.chat_member(
    F.chat.type == ChatType.CHANNEL,
    ChatMemberUpdatedFilter(IS_MEMBER))
async def subscribed_user(
    event: ChatMemberUpdated,
    bot: Bot,
    l10n: TranslatorRunner,
    redis: Redis,
    connect: Connection,
    data_db: DataDB
) -> None:
    sub_chat_id = loads(await redis.get('sub_chat_id'))
    if event.chat.id != sub_chat_id:
        return
    data = await data_db.get_data_to_tid(
        connect, tid=event.from_user.id
    )
    
    await bot.send_message(
        chat_id=data.cid,
        text=l10n.first.url(),
        reply_markup=sign_up(l10n)
    )
    date_time = datetime.now().replace(
        microsecond=0, second=0
    ) + timedelta(minutes=5)
    await data_db.update_data(
        connect,
        tid=data.tid,
        stage=3,
        datetime=date_time
    )
