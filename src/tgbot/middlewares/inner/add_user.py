from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, User

from src.core.dto import AddUserDTO
from src.core.enums import StageType
from src.infrastructure.postgres import DAO
from src.utils import get_datetime


class AddUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user: User = data.get('event_from_user')
        
        if user is None:
            return await handler(event, data)
        
        dao: DAO = data.get('dao')
        await dao.user.add(
            AddUserDTO(
                tid=event.from_user.id,
                cid=event.chat.id,
                stage=StageType.NINE.id,
                datetime=get_datetime(StageType.NINE.delay)
            )
        )
        await handler(event, data)
