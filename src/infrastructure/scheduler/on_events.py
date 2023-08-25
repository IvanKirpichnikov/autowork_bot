from aiogram import Bot
from aiogram.enums import ParseMode
from asyncpg import Pool
from fluentogram import TranslatorHub, TranslatorRunner
from taskiq import TaskiqEvents, TaskiqState

from src.core.configs import config
from src.infrastructure.broker import app
from src.infrastructure.scheduler.app import broker
from src.utils import create_postgres_pool, create_translator_hub


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def worker_startup(state: TaskiqState) -> None:
    bot: Bot = Bot(
        config.tgbot.token,
        parse_mode=ParseMode.HTML
    )
    pool: Pool = await create_postgres_pool(config)
    _hub: TranslatorHub = create_translator_hub()
    l10n: TranslatorRunner = _hub.get_translator_by_locale('ru')
    await app.broker.start()
    state.pool = pool
    state.l10n = l10n
    state.bot = bot
    state.nats = app.broker


@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def worker_shutdown(state: TaskiqState) -> None:
    await state.pool.close()
    await state.bot.session.close()
