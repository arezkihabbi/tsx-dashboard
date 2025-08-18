from enum import Enum
from typing import Union

from .._tools import make_enum_arg_parser
from .._base_enum import StrEnum


class DayIntervalType(Enum):
    INTRA = 0
    INTER = 1


class Intervals(StrEnum):
    """
    The list of interval types of the boundary is described below.

    The supported values of intervals :

        Time:

        Backend will return complete N-minute summaries data.
        When the request start and/or end does not at the N minutes boundary,
        the response will be adjusted.

            MINUTE - return complete 1-minute
            ONE_MINUTE - return complete 1-minute
            FIVE_MINUTES - return complete 5-minutes
            TEN_MINUTES - return complete 10-minutes
            THIRTY_MINUTES - return complete 30-minutes
            SIXTY_MINUTES - return complete 60-minutes
            ONE_HOUR - return complete 1-hour
            HOURLY - return complete 1-hour

        Days:

            DAILY - This is end of day, daily data
            ONE_DAY - This is end of day, daily data
            SEVEN_DAYS - Weekly boundary based on the exchange's
                         week summarization definition
            WEEKLY - Weekly boundary based on the exchange's
            ONE_WEEK - Weekly boundary based on the exchange's
                     week summarization definition
            MONTHLY - Monthly boundary based on calendar month
            ONE_MONTH - Monthly boundary based on calendar month
            THREE_MONTHS - Quarterly boundary based on calendar quarter
            QUARTERLY - Quarterly boundary based on calendar quarter
            TWELVE_MONTHS - Yearly boundary based on calendar year
            YEARLY - Yearly boundary based on calendar year
            ONE_YEAR - Yearly boundary based on calendar year
    """

    MINUTE = "PT1M"
    ONE_MINUTE = "PT1M"
    FIVE_MINUTES = "PT5M"
    TEN_MINUTES = "PT10M"
    THIRTY_MINUTES = "PT30M"
    SIXTY_MINUTES = "PT60M"
    HOURLY = "PT1H"
    ONE_HOUR = "PT1H"
    DAILY = "P1D"
    ONE_DAY = "P7D"
    SEVEN_DAYS = "P7D"
    WEEKLY = "P1W"
    ONE_WEEK = "P1W"
    MONTHLY = "P1M"
    ONE_MONTH = "P1M"
    THREE_MONTHS = "P3M"
    QUARTERLY = "P3M"
    TWELVE_MONTHS = "P12M"
    YEARLY = "P1Y"
    ONE_YEAR = "P1Y"


_ISO8601_INTERVALS = [k for k in Intervals]
"""['PT1M', 'PT5M', 'PT10M', 'PT30M', 'PT60M', 'PT1H']"""
_INTRADAY = _ISO8601_INTERVALS[:6]
"""['P1D', 'P7D', 'P1W', 'P1M', 'P3M', 'P12M', 'P1Y']"""
_INTERDAY = _ISO8601_INTERVALS[6:]

interval_arg_parser = make_enum_arg_parser(Intervals, can_be_lower=True)


def get_day_interval_type(interval: Union[str, Intervals, DayIntervalType]) -> DayIntervalType:
    if isinstance(interval, DayIntervalType):
        return interval

    interval = interval_arg_parser.get_str(interval)

    if interval in _INTRADAY:
        day_interval_type = DayIntervalType.INTRA

    elif interval in _INTERDAY:
        day_interval_type = DayIntervalType.INTER

    else:
        raise TypeError(f"Incorrect day interval, interval={interval}.")

    return day_interval_type
