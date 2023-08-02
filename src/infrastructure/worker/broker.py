from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend

from config import Config


redis = Config.redis
print(redis)
url = f"redis://:{redis.password.get_secret_value()}@{redis.host}:{redis.port}"
redis_async_result = RedisAsyncResultBackend( 
    redis_url=url
)
broker = ListQueueBroker( 
    url=url
).with_result_backend(
    redis_async_result
)
