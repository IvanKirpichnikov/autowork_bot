class NotFoundChatIDLogsGroup(Exception):
    def __str__(self):
        return "the chat id group for logs was not found in the redis by the key 'logs_chat_id'"
