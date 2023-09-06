from asyncio import sleep
from json import loads

from aiogram import Bot, Router, F
from aiogram.exceptions import TelegramRetryAfter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from asyncpg import Connection
from redis.asyncio.client import Redis

from src.bot.keyboards.inline import keyboard_scroll
from src.infrastructure.database.db.data import DataDB


router = Router()

TEXT = (
    'айди: {id}\n'
    'тг логин: {username}\n'
    'дата регистрации: {datetime}\n'
    'этап: {stage}'
)


def get_stage_text(stage: int) -> str:
    match stage:
        case 1:
            return 'Прошел все этапы'
        case 2:
            return 'Повторно просим подписаться'
        case 3:
            return 'Ждет отправление первого урока'
        case 4:
            return 'Ждет комментарии к первому уроку'
        case 5:
            return 'Ждет отправление второго урока'
        case 6:
            return 'Ждет отправления опроса'
        case 8:
            return 'Ждет отправления третьего урока'
        case 9:
            return 'Ждет комментарии к первому уроку'


#
@router.message(F.text == '/user', #F.from_user.id.in_({261868831, 1138290849})
)
async def start(
    message: Message,
    connect: Connection,
    data_db: DataDB,
    redis: Redis,
    bot: Bot
) -> None:
    chat_id = loads(await redis.get('log_chat_id'))
    data = await data_db.pagination(connect, offset=0)
    
    for _ in data:
        try:
            await sleep(0.5)
            await bot.send_message(
                chat_id=chat_id,
                text=TEXT.format(
                    id=_.id,
                    username=_.username,
                    datetime=_.registration,
                    stage=get_stage_text(_.stage)
                ),
            )
        except TelegramRetryAfter as e:
            print(e)
            await sleep(e.retry_after)
    
    await message.answer('Финиш')