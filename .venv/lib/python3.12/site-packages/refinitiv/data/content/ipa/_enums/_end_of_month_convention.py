from enum import unique
from ...._base_enum import StrEnum


@unique
class EndOfMonthConvention(StrEnum):
    """
    End of month convention.

    The possible values are:
        - Last,
        - Same,
        - Last28,
        - Same28
    """

    LAST = "Last"
    LAST28 = "Last28"
    SAME = "Same"
    SAME28 = "Same28"
