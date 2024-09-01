import logging

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
    logging.info(f"Group subscribed to notifications [Group ID:{group_id}]")


@router.message(
    Command("unsubscribe"),
    ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP]),
    AdminFilter(),
)
async def unsubscribe(message: Message) -> None:
    group_id = str(message.chat.id)
    await group_service.remove_group(group_id)
    await message.answer("Unsubscribed succesfully!")
    logging.info(f"Group unsubscribed from notifications [Group ID:{group_id}]")
