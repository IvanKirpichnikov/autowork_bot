from typing import NewType

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from fluentogram import TranslatorRunner


URL = NewType('URL', str)


class MoreCD(CallbackData, prefix='more'):
    video: int


def sign_up(l10n: TranslatorRunner) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.button(
        text=l10n.sign.up(), callback_data='JdiWijCjeo'
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
        )
    )
    builder.button(
        text=l10n.sign.up(), callback_data='JdiWijCjeo'
    )
    
    return builder.adjust(1).as_markup()

def get_access(l10n: TranslatorRunner) -> InlineKeyboardMarkup:
    bilder = InlineKeyboardBuilder()
    
    bilder.button(
        text=l10n.sub.to.channel(), url=l10n.channel.url()
    )
    return bilder.as_markup()

def pool() -> InlineKeyboardMarkup:
    bilder = InlineKeyboardBuilder()
    
    bilder.button(
        text='1', callback_data='shcijjd3'
    )
    for _ in range(2, 4):
        bilder.button(
            text=str(_), callback_data=f'shcijjd{_-1}'
        )
    return bilder.as_markup()
