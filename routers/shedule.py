from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from utils import get_day_week, prepare_schedule_msg


router = Router()


@router.message(Command("today"))
async def get_today_schedule(message: Message):
    day_of_week_number, week_number = get_day_week()

    msg = prepare_schedule_msg(day_of_week_number, week_number)
    await message.answer(f"Schedule:\n\n{msg}")


@router.message(Command("tomorrow"))
async def get_tommorrow_schedule(message: Message):
    day_of_week_number, week_number = get_day_week()

    if (next_day := day_of_week_number + 1) >= 6:
        next_day = 0
        week_number += 1

    msg = prepare_schedule_msg(next_day, week_number)
    await message.answer(f"Schedule:\n\n{msg}")
