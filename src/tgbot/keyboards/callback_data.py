from aiogram.filters.callback_data import CallbackData


class MoreCD(CallbackData, prefix='more'):
    video: int
