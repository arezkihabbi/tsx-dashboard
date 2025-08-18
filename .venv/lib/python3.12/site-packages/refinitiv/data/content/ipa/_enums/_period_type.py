from enum import unique

from ...._base_enum import StrEnum


@unique
class PeriodType(StrEnum):
    """
    The method we chose to count the period of time:

    The possible values are:
        - WorkingDay (consider only working days),
        - NonWorkingDay (consider only non working days),
        - Day (consider all days),
        - Year (consider year),
        - NearestTenor (returns the nearest tenor for the given period)
    """

    WORKING_DAY = "WorkingDay"
    NON_WORKING_DAY = "NonWorkingDay"
    DAY = "Day"
    YEAR = "Year"
    NEAREST_TENOR = "NearestTenor"
