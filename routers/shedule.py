import logging

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from utils import get_day_week, prepare_schedule_msg


router = Router()


def get_logger_msg(text: str, message: Message) -> str:
    group_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username

    return f"{text} [Group ID:{group_id}] [User ID:{user_id}] [Username:{username}]"


@router.message(Command("today"))
async def get_today_schedule(message: Message):
    day_of_week_number, week_number = get_day_week()

    msg = prepare_schedule_msg(day_of_week_number, week_number)
    await message.answer(msg)

    logging.info(get_logger_msg("Send today's schedule", message))


@router.message(Command("tomorrow"))
async def get_tommorrow_schedule(message: Message):
    day_of_week_number, week_number = get_day_week()

    if (next_day := day_of_week_number + 1) >= 6:
        next_day = 0
        week_number += 1

    msg = prepare_schedule_msg(next_day, week_number)
    await message.answer(msg)
    logging.info(get_logger_msg("Send tomorrow's schedule", message))
