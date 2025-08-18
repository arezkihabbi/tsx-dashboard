from enum import unique

from ....._base_enum import StrEnum


@unique
class CalendarAdjustment(StrEnum):
    FALSE = "False"
    NULL = "None"
    WEEKEND = "Weekend"
    CALENDAR = "Calendar"
