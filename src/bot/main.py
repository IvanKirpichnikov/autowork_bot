from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisEventIsolation, RedisStorage
from asyncpg import Pool
from fluent_compiler.bundle import FluentBundle
from fluentogram import TranslatorHub, FluentTranslator
from redis.asyncio import Redis

from config import Config
from src.bot.handlers.routers import router
from src.bot.middlewares.l10n import L10NMiddleware
from src.bot.middlewares.trottling import TrottlingMiddleware
from src.bot.middlewares.create_connect import CreateConnectMiddleware
from src.infrastructure.database.db.data import DataDB


async def start_bot(
    pool: Pool,
    redis: Redis,
    config: Config
):
    hub = TranslatorHub(
        dict(
            ru=('ru',)
        ),
        [
            FluentTranslator(
                'ru', FluentBundle.from_files(
                    'ru-RU',
                    filenames=[
                        'locales/ru/txt.ftl'
                    ]
                )
            )
        ],
        root_locale='ru'
    )
    
    bot = Bot(
        config.bot.token.get_secret_value(),
        parse_mode='html'
    )
    if config.bot.skip_updates:
        await bot.delete_webhook(drop_pending_updates=True)
    
    dp = Dispatcher(
        storage=RedisStorage(
            redis,
            key_builder=DefaultKeyBuilder(
                with_destiny=True
            )
        ),
        events_isolation=RedisEventIsolation(redis)
    )
    dp.include_router(router)
    
    dp.message.outer_middleware(TrottlingMiddleware())
    dp.message.middleware(L10NMiddleware())
    dp.my_chat_member.middleware(L10NMiddleware())
    dp.callback_query.middleware(L10NMiddleware())
    dp.callback_query.outer_middleware(TrottlingMiddleware())
    dp.chat_member.middleware(L10NMiddleware())
    dp.update.middleware(CreateConnectMiddleware())
    
    dp['data_db'] = DataDB()
    dp['pool'] = pool
    dp['redis'] = redis
    dp['_hub'] = hub
    
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
