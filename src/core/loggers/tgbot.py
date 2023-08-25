from logging import getLogger
from logging.handlers import RotatingFileHandler

from src.core.loggers.handler import stream_handler


tgbot = getLogger('autowork.tgbot')

# file_handler = RotatingFileHandler(
#     filename='logs/tgbot/tgbot.log',
#     maxBytes=10000,
#     backupCount=100000,
#     encoding='utf-8',
#     mode='w'
# )
tgbot.addHandler(stream_handler)
# tgbot.addHandler(file_handler)
