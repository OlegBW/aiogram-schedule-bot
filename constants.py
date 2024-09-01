from enum import Enum
import pytz

GROUPS_FILE = "groups.json"
TIMEZONE = pytz.timezone("Europe/Kyiv")


class WeekType(Enum):
    numerator = 0
    denominator = 1
