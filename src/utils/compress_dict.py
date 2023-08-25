from typing import TypeVar, Union

import lz4.frame
from orjson import dumps


ByteArray = TypeVar('ByteArray')


def compress_dict(**kwargs) -> Union[bytes, ByteArray]:
    return lz4.frame.compress(
        dumps(kwargs)
    )
