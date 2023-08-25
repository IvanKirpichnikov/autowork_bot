from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery
from fluentogram import TranslatorRunner

from src.core.loggers import tgbot


router = Router(name='admin/sign/up/router')


@router.callback_query(F.data == 'JdiWijCjeo')
async def user_contact(
    callback: CallbackQuery,
    bot: Bot,
    l10n: TranslatorRunner,
    log_chat_id: int
) -> None:
    await callback.message.answer(
        l10n.user.contact()
    )
    await bot.send_message(
        log_chat_id,
        l10n.admin.contact(
            username=f'@{callback.from_user.username}',
        )
    )
    await callback.answer()
    tgbot.info(
        'User signs up for an event. User ID=%r',
        callback.from_user.id
    )
