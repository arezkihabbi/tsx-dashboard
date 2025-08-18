from enum import unique
from ...._base_enum import StrEnum


@unique
class TimeStamp(StrEnum):
    CLOSE = "Close"
    CLOSE_LONDON5_PM = "CloseLondon5PM"
    CLOSE_NEW_YORK5_PM = "CloseNewYork5PM"
    CLOSE_TOKYO5_PM = "CloseTokyo5PM"
    DEFAULT = "Default"
    OPEN = "Open"
    SETTLE = "Settle"
