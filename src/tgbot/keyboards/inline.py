from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from fluentogram import TranslatorRunner

from src.tgbot.keyboards.callback_data import MoreCD


def sign_up(l10n: TranslatorRunner) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=l10n.inline.sign.up(),
        callback_data='JdiWijCjeo'
    )
    
    return builder.as_markup()


def more_and_sign_up(
    l10n: TranslatorRunner,
    video: int,
    text: str
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=text,
        callback_data=MoreCD(
            video=video
        ).pack()
    )
    builder.button(
        text=l10n.inline.sign.up(),
        callback_data='JdiWijCjeo'
    )
    
    return builder.adjust(1).as_markup()


def get_access(l10n: TranslatorRunner) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=l10n.inline.sub.channel(),
        url=l10n.url.channel()
    )
    return builder.as_markup()


def poll() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='1',
        callback_data='shcijjd3'
    )
    for value in range(2, 4):
        builder.button(
            text=str(value),
            callback_data=f'shcijjd{value - 1}'
        )
    
    return builder.as_markup()
