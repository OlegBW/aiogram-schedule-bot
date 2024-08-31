import asyncio
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

from bot import bot
from services import GroupService
from routers import subscriptions_router

from constants import WeekType
from data import schedule

group_service = GroupService()

dp = Dispatcher()
dp.include_routers(subscriptions_router)


def prepare_schedule_msg(day: int, week_number: int) -> str:
    daily_schedule = schedule[day]
    week_type: WeekType = (
        WeekType.numerator if week_number % 2 == 0 else WeekType.denominator
    ).value

    msg_lines = []
    for time_slot, subjects in daily_schedule.items():
        if week_type < len(subjects):
            msg_lines.append(f"{time_slot}: {subjects[week_type]}")

    if not msg_lines:
        return "Weekend"

    return "\n".join(msg_lines)


async def send_scheduled_msg(bot: Bot):
    group_ids = await group_service.get_groups()

    now = datetime.now()
    day_of_week_number = now.weekday()
    week_number = now.isocalendar()[1]

    msg = prepare_schedule_msg(day_of_week_number, week_number)

    for group_id in group_ids:
        try:
            resp_msg = await bot.send_message(
                chat_id=group_id, text=f"Schedule:\n\n{msg}"
            )
            await bot.pin_chat_message(group_id, resp_msg.message_id)
        except TelegramForbiddenError:
            await group_service.remove_group(str(group_id))
            pass
        except TelegramBadRequest:
            pass


async def main():
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        send_scheduled_msg,
        trigger="cron",
        hour=5,
        minute=0,
        start_date=datetime.now(),
        kwargs={
            "bot": bot,
        },
    )

    scheduler.start()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main=main())
