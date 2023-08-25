from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import ADMINISTRATOR, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated
from redis.asyncio import Redis

from src.core.loggers import tgbot


router = Router(name='admin/set/channel/router')


@router.my_chat_member(
    F.chat.type == ChatType.CHANNEL,
    ChatMemberUpdatedFilter(ADMINISTRATOR)
)
async def set_sub_chat(
    event: ChatMemberUpdated,
    redis: Redis
) -> None:
    chat_id = event.chat.id
    
    await redis.set('sub_chat_id', chat_id)
    tgbot.warning(
        'Setup new subscribe chat. Chat ID=%r',
        chat_id
    )


@router.my_chat_member(
    F.chat.type.in_(
        {
            ChatType.GROUP.value,
            ChatType.SUPERGROUP.value
        }
    ),
    ChatMemberUpdatedFilter(ADMINISTRATOR)
)
async def set_log_chat(
    event: ChatMemberUpdated,
    redis: Redis
) -> None:
    chat_id = event.chat.id
    
    await redis.set('log_chat_id', chat_id)
    tgbot.warning(
        'Setup new log chat. Chat ID=%r',
        chat_id
    )
