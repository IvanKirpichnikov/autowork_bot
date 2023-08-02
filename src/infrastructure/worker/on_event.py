from aiogram import Bot
from asyncpg import create_pool
from taskiq import TaskiqEvents, TaskiqState
from fluent_compiler.bundle import FluentBundle
from fluentogram import TranslatorHub, FluentTranslator

from config import Config
from src.infrastructure.database.db.data import DataDB
from src.infrastructure.worker.broker import broker


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def worker_startup(state: TaskiqState) -> None:
    config = Config
    psql = config.psql
    pool = await create_pool(
        host=psql.host,
        port=psql.port,
        user=psql.user,
        password=psql.password.get_secret_value(),
        database=psql.database
    )
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
    state.bot = Bot(
        Config.bot.token.get_secret_value(),
        parse_mode='html'
    )
    state.data_db = DataDB()
    state.pool = pool
    state.l10n = hub.get_translator_by_locale('ru')

@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def worker_shutdown(state: TaskiqState) -> None:
    await state.pool.close()
    await state.bot.session.close()
