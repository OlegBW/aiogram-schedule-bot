import asyncio
from datetime import datetime
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import BotCommand

from bot import bot
from services import GroupService
from routers import subscriptions_router, schedule_router

from utils import get_day_week, prepare_schedule_msg
from constants import TIMEZONE

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

group_service = GroupService()

dp = Dispatcher()
dp.include_routers(subscriptions_router, schedule_router)


async def on_startup(bot: Bot):
    commands = [
        BotCommand(
            command="/subscribe", description="Subscribe to the schedule notification"
        ),
        BotCommand(
            command="/unsubscribe",
            description="Unsubscribe from the schedule notification",
        ),
        BotCommand(command="/today", description="Get today's schedule"),
        BotCommand(
            command="/tomorrow",
            description="Get the tomorrow's schedule",
        ),
    ]

    await bot.set_my_commands(commands)


async def send_scheduled_msg(bot: Bot):
    group_ids = await group_service.get_groups()

    day_of_week_number, week_number = get_day_week()

    msg = prepare_schedule_msg(day_of_week_number, week_number)

    for group_id in group_ids:
        try:
            resp_msg = await bot.send_message(chat_id=group_id, text=msg)
            logging.info(f"Send scheduled message [Group ID::{group_id}]")
            await bot.pin_chat_message(group_id, resp_msg.message_id)
            logging.info(f"Pin sended message [Group ID::{group_id}]")
        except TelegramForbiddenError:
            await group_service.remove_group(str(group_id))
            pass
        except TelegramBadRequest:
            pass


async def main():
    await on_startup(bot)

    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        send_scheduled_msg,
        trigger="cron",
        hour=5,
        minute=0,
        start_date=datetime.now(TIMEZONE),
        kwargs={
            "bot": bot,
        },
    )

    scheduler.start()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main=main())
