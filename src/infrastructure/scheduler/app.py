import logging

from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend

from src.core.configs import config


logging.basicConfig(level=logging.DEBUG)
redis = config.redis
url = f"redis://:{redis.password}@{redis.host}:{redis.port}/2"
broker = ListQueueBroker(url=url).with_result_backend(
    RedisAsyncResultBackend(redis_url=url)
)
scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)]
)
