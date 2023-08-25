from typing import NewType

from src.core.configs import Config


def create_nats_url(config: Config) -> str:
    nats = config.nats
    return f'nats://{nats.user}:{nats.password}@{nats.server}:{nats.port}'
