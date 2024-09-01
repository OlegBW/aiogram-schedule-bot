from datetime import datetime
from typing import Tuple

from data import schedule
from constants import WeekType


def get_day_week() -> Tuple[int, int]:
    now = datetime.now()
    day_of_week_number = now.weekday()
    week_number = now.isocalendar()[1]

    return day_of_week_number, week_number


def prepare_schedule_msg(day: int, week_number: int) -> str:
    daily_schedule = schedule[day]
    week_type: WeekType = (
        WeekType.denominator if week_number % 2 == 0 else WeekType.numerator
    ).value

    msg_lines = []
    for time_slot, subjects in daily_schedule.items():
        if week_type < len(subjects):
            msg_lines.append(f"📒 {time_slot}: {subjects[week_type]}")

    if not msg_lines:
        return "🎆 Weekend"
    
    raw_schedule = "\n\n".join(msg_lines)

    return f"📆 Schedule:\n\n{raw_schedule}"
