from enum import unique

from ....._base_enum import StrEnum


@unique
class StrikeType(StrEnum):
    ABSOLUTE_PERCENT = "AbsolutePercent"
    RELATIVE_PERCENT = "RelativePercent"
