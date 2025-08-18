from enum import unique

from ......_base_enum import StrEnum


@unique
class CalendarAdjustment(StrEnum):
    CALENDAR = "Calendar"
    FALSE = "False"
    WEEKEND = "Weekend"
