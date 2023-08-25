from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from asyncpg import Pool
from redis.asyncio import Redis

from src.core.configs import Config
from src.tgbot.handlers.routers import router
from src.tgbot.middlewares.inner import AddUserMiddleware, DAOMiddleware, L10NMiddleware, ThrottlingMiddleware
from src.tgbot.middlewares.outer import TransferDataOuterMiddleware
from src.utils import create_translator_hub


async def start_bot(
    pool: Pool,
    redis: Redis,
    config: Config
):
    bot = Bot(
        config.tgbot.token,
        parse_mode='html'
    )
    if config.tgbot.skip_updates:
        await bot.delete_webhook(drop_pending_updates=True)
    
    storage = RedisStorage(
        redis,
        key_builder=DefaultKeyBuilder(
            with_destiny=True
        )
    )
    dp = Dispatcher(
        storage=storage,
        events_isolation=storage.create_isolation()
    )
    dp.include_router(router)
    
    dp.update.outer_middleware(TransferDataOuterMiddleware(redis))
    
    dp.update.middleware(DAOMiddleware(pool))
    dp.update.middleware(L10NMiddleware(create_translator_hub()))
    dp.message.middleware(ThrottlingMiddleware())
    dp.message.middleware(AddUserMiddleware())
    dp.callback_query.middleware(ThrottlingMiddleware())
    
    dp['pool'] = pool
    dp['redis'] = redis
    
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
