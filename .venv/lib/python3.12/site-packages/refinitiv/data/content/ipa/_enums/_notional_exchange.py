from enum import unique
from ...._base_enum import StrEnum


@unique
class NotionalExchange(StrEnum):
    BOTH = "Both"
    END = "End"
    END_ADJUSTMENT = "EndAdjustment"
    NONE = "None"
    START = "Start"
