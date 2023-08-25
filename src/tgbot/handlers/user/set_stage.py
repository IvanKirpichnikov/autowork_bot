from aiogram import Bot, F, Router
from aiogram.enums import ChatType
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION, KICKED, MEMBER
from aiogram.types import ChatMemberUpdated
from fluentogram import TranslatorRunner

from src.core.dto import AddUserDTO, DeleteUserDTO, GetUserByIDDTO, UpdateUserDTO
from src.core.enums import StageType
from src.infrastructure.postgres import DAO
from src.tgbot.keyboards.inline import sign_up
from src.utils import get_datetime


router = Router(name=__name__)


@router.my_chat_member(
    F.chat.type == ChatType.PRIVATE,
    ChatMemberUpdatedFilter(KICKED >> MEMBER)
)
async def add_user(
    event: ChatMemberUpdated,
    dao: DAO
) -> None:
    await dao.user.add(
        AddUserDTO(
            tid=event.from_user.id,
            cid=event.chat.id,
            stage=StageType.ONE.id,
            datetime=get_datetime(StageType.ONE.delay)
        )
    )


@router.my_chat_member(
    F.chat.type == ChatType.PRIVATE,
    ChatMemberUpdatedFilter(MEMBER >> KICKED)
)
async def delete_user(
    event: ChatMemberUpdated,
    dao: DAO
) -> None:
    await dao.user.delete(
        DeleteUserDTO(tid=event.from_user.id)
    )


@router.chat_member(
    F.chat.type == ChatType.CHANNEL,
    ChatMemberUpdatedFilter(JOIN_TRANSITION)
)
async def subscribed_user(
    event: ChatMemberUpdated,
    bot: Bot,
    l10n: TranslatorRunner,
    dao: DAO,
    sub_chat_id: int
) -> None:
    if event.chat.id != sub_chat_id:
        return
    
    data = await dao.user.get_by_tid(
        GetUserByIDDTO(tid=event.from_user.id)
    )
    
    await bot.send_message(
        chat_id=data.cid,
        text=l10n.url.first(),
        reply_markup=sign_up(l10n)
    )
    await dao.user.update(
        UpdateUserDTO(
            tid=data.tid,
            stage=StageType.THREE.id,
            datetime=get_datetime(StageType.TWO.delay)
        )
    )
