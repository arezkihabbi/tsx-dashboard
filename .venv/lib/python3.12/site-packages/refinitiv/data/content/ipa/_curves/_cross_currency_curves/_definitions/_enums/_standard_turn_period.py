from enum import unique

from ......._base_enum import StrEnum


@unique
class StandardTurnPeriod(StrEnum):
    NONE = "None"
    QUARTER_ENDS = "QuarterEnds"
    YEAR_ENDS = "YearEnds"
