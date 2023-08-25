from aiogram import Bot
from aiogram.enums import ParseMode
from asyncpg import Pool
from fluentogram import TranslatorHub, TranslatorRunner
from propan import Context, ContextRepo, NatsBroker, PropanApp, Depends

from src.core.configs import config
from src.core.dto import UserPubDTO
from src.infrastructure.broker.decode_message import decode_and_validation
from src.infrastructure.broker.subjects import files
from src.utils import create_nats_url, create_postgres_pool, create_translator_hub


broker = NatsBroker(
    create_nats_url(config),
    decode_message=decode_and_validation(UserPubDTO),

)
for file in files:
    broker.include_router(file.router)

app = PropanApp(broker)


@app.on_startup
async def set_data(context: ContextRepo = Context()) -> None:
    bot: Bot = Bot(config.tgbot.token, parse_mode=ParseMode.HTML)
    _hub: TranslatorHub = create_translator_hub()
    l10n: TranslatorRunner = _hub.get_translator_by_locale('ru')
    pool: Pool = await create_postgres_pool(config)
    
    app.context.set_global('bot', bot)
    app.context.set_global('l10n', l10n)
    app.context.set_global('pool', pool)


@app.on_shutdown
async def close_data(
    bot: Bot = Context('bot'),
    pool: Pool = Context('pool')
) -> None:
    await bot.session.close()
    await pool.close()
