from logging import getLogger
from logging.handlers import RotatingFileHandler

from src.core.loggers.handler import stream_handler


broker = getLogger('autowork.broker')

# file_handler = RotatingFileHandler(
#     filename='logs/broker/broker.log',
#     maxBytes=10000,
#     backupCount=100000,
#     encoding='utf-8',
#     mode='w'
# )
broker.addHandler(stream_handler)
# broker.addHandler(file_handler)
