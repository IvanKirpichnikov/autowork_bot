from logging import StreamHandler

from src.core.loggers.formatter import formatter


stream_handler = StreamHandler()
stream_handler.setFormatter(formatter)
