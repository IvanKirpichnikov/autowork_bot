from dataclasses import dataclass

from adaptix import name_mapping, NameStyle, Retort
from dynaconf import Dynaconf


@dataclass(frozen=True)
class _TgBotConfig:
    token: str
    skip_updates: bool


@dataclass(frozen=True)
class _PostgresQLConfig:
    host: str
    port: int
    user: str
    password: str
    database: str


@dataclass(frozen=True)
class _RedisConfig:
    host: str
    port: int
    password: str
    db: int


@dataclass(frozen=True)
class _NatsConfig:
    server: str
    port: int
    user: str
    password: str


@dataclass(frozen=True)
class Config:
    tgbot: _TgBotConfig
    psql: _PostgresQLConfig
    redis: _RedisConfig
    nats: _NatsConfig


dynaconf = Dynaconf(settings_files=['configs/config.toml'])
retort = Retort(recipe=[name_mapping(Config, name_style=NameStyle.UPPER)])

config = retort.load(dynaconf.as_dict(), Config)
