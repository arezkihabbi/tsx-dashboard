from enum import unique

from ...._base_enum import StrEnum


@unique
class IndexAverageMethod(StrEnum):
    ARITHMETIC_AVERAGE = "ArithmeticAverage"
    COMPOUNDED_ACTUAL = "CompoundedActual"
    COMPOUNDED_AVERAGE_RATE = "CompoundedAverageRate"
    DAILY_COMPOUNDED_AVERAGE = "DailyCompoundedAverage"
