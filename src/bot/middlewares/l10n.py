from typing import Awaitable, Callable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Message
from fluentogram import TranslatorHub


class L10NMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, any]
    ):
        hub: TranslatorHub = data.get('_hub')
        lang = event.from_user.language_code
        data['l10n'] = hub.get_translator_by_locale(lang)
        
        return await handler(event, data)
