from logging import Formatter


formatter = Formatter(
    '[$asctime - $name] [$levelname] [$filename - $funcName - $message]',
    datefmt='%d.%m.%Y %H:%M:%S',
    style='$'
)
