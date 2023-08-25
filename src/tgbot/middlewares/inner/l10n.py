from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from fluentogram.src.abc import AbstractTranslatorsHub


class L10NMiddleware(BaseMiddleware):
    def __init__(self, hub: AbstractTranslatorsHub) -> None:
        self._hub = hub
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, any]
    ) -> Any:
        data['l10n'] = self._hub.get_translator_by_locale('ru')
        
        return await handler(event, data)
