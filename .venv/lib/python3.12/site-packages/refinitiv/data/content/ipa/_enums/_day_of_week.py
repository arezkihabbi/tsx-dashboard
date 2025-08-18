from enum import unique
from ...._base_enum import StrEnum


@unique
class DayOfWeek(StrEnum):
    """
    The day of week to which dates are adjusted.
    The first date in the list is defined as corresponding day of week following the start date.
    The last date in the list is defined as corresponding day of week preceding the end date.

    The possible values are:
        - Sunday,
        - Monday,
        - Tuesday,
        - Wednesday,
        - Thursday,
        - Friday,
        - Saturday
    """

    SUNDAY = "Sunday"
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
