from aiogram.filters import Filter
from aiogram.types import Message
from bot import bot


class AdminFilter(Filter):
    async def is_chat_admin(self, chat_id: str | int, user_id: str | int) -> bool:
        admins = await bot.get_chat_administrators(chat_id)

        for admin in admins:
            if admin.user.id == int(user_id):
                return True

        return False

    async def __call__(self, message: Message):
        is_admin = await self.is_chat_admin(message.chat.id, message.from_user.id)
        print(is_admin)
        return is_admin
