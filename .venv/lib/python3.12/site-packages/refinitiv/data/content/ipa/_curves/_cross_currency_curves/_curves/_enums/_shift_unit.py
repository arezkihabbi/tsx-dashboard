from enum import unique

from refinitiv.data._base_enum import StrEnum


@unique
class ShiftUnit(StrEnum):
    ABSOLUTE = "Absolute"
    BP = "Bp"
    PERCENT = "Percent"
