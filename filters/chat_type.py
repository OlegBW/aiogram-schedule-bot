from aiogram.filters import Filter
from aiogram.types import Message
from typing import List
from aiogram.enums import ChatType


class ChatTypeFilter(Filter):
    def __init__(self, chat_types: List[ChatType]):
        self.chat_types = chat_types

    async def __call__(self, message: Message) -> bool:
        return message.chat.type in self.chat_types
