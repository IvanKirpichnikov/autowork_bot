from json import loads

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery
from redis.asyncio import Redis
from fluentogram import TranslatorRunner


router = Router()


@router.callback_query(F.data == 'JdiWijCjeo')
async def user_contact(
    callback: CallbackQuery,
    bot: Bot,
    l10n: TranslatorRunner,
    redis: Redis
) -> None:
    chat_id = loads(await redis.get('log_chat_id'))
    
    await callback.message.answer(
        l10n.user.contact()
    )
    await bot.send_message(
        chat_id,
        l10n.admin.contact(
            username=f'@{callback.from_user.username}',
        )
    )
    await callback.answer()
