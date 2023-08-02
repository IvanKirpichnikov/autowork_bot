from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import ChatMemberUpdatedFilter, ADMINISTRATOR
from aiogram.types import ChatMemberUpdated
from redis.asyncio import Redis


router = Router()


@router.my_chat_member(
    F.chat.type == ChatType.CHANNEL,
    ChatMemberUpdatedFilter(ADMINISTRATOR)
)
async def set_chat_id(
    event: ChatMemberUpdated,
    redis: Redis
) -> None:
    chat_id = event.chat.id
    await redis.set('sub_chat_id', chat_id)

@router.my_chat_member(
    F.chat.type.in_(
        {
            ChatType.GROUP.value,
            ChatType.SUPERGROUP.value
        }
    ),
    ChatMemberUpdatedFilter(ADMINISTRATOR)
)
async def set_log_chat_id(
    event: ChatMemberUpdated,
    redis: Redis
) -> None:
    chat_id = event.chat.id
    await redis.set('log_chat_id', chat_id)
