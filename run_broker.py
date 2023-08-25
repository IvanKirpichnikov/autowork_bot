import asyncio

from src.infrastructure.broker import app


asyncio.run(app.run())