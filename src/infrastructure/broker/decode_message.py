from typing import Callable, TypeVar

import lz4.frame
from nats.aio.msg import Msg
from orjson import loads
from propan import PropanMessage
from propan.types import DecodedMessage

from src.core.dto import user_pub_retort


_T = TypeVar('_T')
OriginalDecode = Callable[[PropanMessage[Msg]], DecodedMessage]


def decode_and_validation(dataclass: _T) -> Callable[[PropanMessage[Msg], OriginalDecode], _T]:
    async def decode_wrapper(message: PropanMessage, _: OriginalDecode) -> _T:
        data = loads(
            lz4.frame.decompress(message.body)
        )
        return user_pub_retort.load(data, dataclass)
    
    return decode_wrapper
