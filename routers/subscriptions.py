from aiogram import Router
from aiogram.filters import Command
from aiogram.enums import ChatType
from aiogram.types import Message

from filters import ChatTypeFilter, AdminFilter
from services import GroupService

router = Router()
group_service = GroupService()


@router.message(
    Command("subscribe"),
    ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP]),
    AdminFilter(),
)
async def subscribe(message: Message) -> None:
    group_id = str(message.chat.id)
    await group_service.add_group(group_id)
    await message.answer("Subscribed succesfully!")


@router.message(
    Command("unsubscribe"),
    ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP]),
    AdminFilter(),
)
async def unsubscribe(message: Message) -> None:
    # print(message)
    group_id = str(message.chat.id)
    print(group_id)
    await group_service.remove_group(group_id)
    await message.answer("Unsubscribed succesfully!")
