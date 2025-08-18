from enum import unique

from refinitiv.data._base_enum import StrEnum


@unique
class ShiftType(StrEnum):
    ADDITIVE = "Additive"
    RELATIVE = "Relative"
    RELATIVE_PERCENT = "RelativePercent"
    SCALED = "Scaled"
