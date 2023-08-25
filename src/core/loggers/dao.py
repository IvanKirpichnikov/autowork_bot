from logging import getLogger
from logging.handlers import RotatingFileHandler

from src.core.loggers.handler import stream_handler


dao = getLogger('autowork.dao')

# file_handler = RotatingFileHandler(
#     filename='logs/dao/dao.log',
#     maxBytes=10000,
#     backupCount=100000,
#     encoding='utf-8',
#     mode='w'
# )
dao.addHandler(stream_handler)
# dao.addHandler(file_handler)
