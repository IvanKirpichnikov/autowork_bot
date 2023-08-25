from logging import getLogger
from logging.handlers import RotatingFileHandler

from src.core.loggers.handler import stream_handler


scheduler = getLogger('autowork.scheduler')

# file_handler = RotatingFileHandler(
#     filename='logs/scheduler/scheduler.log',
#     maxBytes=10000,
#     backupCount=100000,
#     encoding='utf-8',
#     mode='w'
# )
scheduler.addHandler(stream_handler)
# scheduler.addHandler(file_handler)
