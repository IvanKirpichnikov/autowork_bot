class AutoWorkException(Exception):
    pass


class ChatGroupIDNotFoundForLogs(AutoWorkException):
    def __str__(self):
        return "the chat id group for log was not found in the redis by the key 'log_chat_id'"


class ChatGroupIDNotFoundForSub(AutoWorkException):
    def __str__(self):
        return "the chat id group for sub was not found in the redis by the key 'sub_chat_id'"
