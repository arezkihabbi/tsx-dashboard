from enum import unique

from ...._base_enum import StrEnum


@unique
class DateScheduleFrequency(StrEnum):
    """
    The frequency of dates in the predefined period. The possible values are:

    The possible values are:
        - Daily,
        - Weekly,
        - BiWeekly,
        - Monthly,
    """

    DAILY = "Daily"
    WEEKLY = "Weekly"
    BI_WEEKLY = "BiWeekly"
    MONTHLY = "Monthly"
