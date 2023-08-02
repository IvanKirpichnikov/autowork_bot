from pydantic import BaseSettings, Field, SecretStr


class BaseConfig(BaseSettings):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

class _BotConfig(BaseConfig):
    token: SecretStr
    skip_updates: bool

class _PostgresQLConfig(BaseConfig):
    host: str = Field(env='psql_host')
    port: int = Field(env='psql_port')
    user: str = Field(env='psql_user')
    password: SecretStr = Field(env='psql_password')
    database: str = Field(env='psql_database')

class _RedisConfig(BaseConfig):
    host: str = Field(env='redis_host')
    port: int = Field(env='redis_port')
    password: SecretStr = Field(env='redis_password')
    db: int = Field(env='redis_db')

class _NatsConfig(BaseConfig):
    server: str = Field(env='nats_server')
    port: int = Field(env='nats_port')
    user: str = Field(env='nats_user')
    password: SecretStr = Field(env='nats_password')

class Config:
    bot = _BotConfig()
    psql = _PostgresQLConfig()
    redis = _RedisConfig()
    nats = _NatsConfig()
