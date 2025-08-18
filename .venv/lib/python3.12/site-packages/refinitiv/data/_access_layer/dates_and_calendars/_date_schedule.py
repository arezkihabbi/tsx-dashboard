from typing import List, Optional, Union

import numpy as np

from ..._types import OptDateTime
from ...content.ipa._enums import DateScheduleFrequency, DayOfWeek
from ...content.ipa.dates_and_calendars.date_schedule import Definition


def date_schedule(
    frequency: Union[DateScheduleFrequency, str] = None,
    start_date: "OptDateTime" = None,
    end_date: "OptDateTime" = None,
    calendar_day_of_month: Optional[int] = None,
    calendars: Optional[List[str]] = None,
    currencies: Optional[List[str]] = None,
    day_of_week: Optional[Union[DayOfWeek, str]] = None,
    count: Optional[int] = None,
) -> List[np.datetime64]:
    """
    Gets a list of dates based on the provided values, which can then be used as input for other functions.

    Parameters
    ----------
        frequency: DateScheduleFrequency or str, optional
            The frequency of dates in the predefined period.
        start_date: str or datetime or timedelta, optional
            The start date of the predetermined list of dates.
            The start date must be earlier or equal to the end date.
            Mandatory if endDate is in the past.
        end_date: str or datetime or timedelta, optional
            The end date of the predetermined list of dates.
            If start_date is not set end_date is used to
            define a list of dates from today to the end date;
            end_date and count should not be set at a time;
            end_date must be later or equal to start_date.
            Mandatory if count is not specified.
        calendar_day_of_month : int, optional
            The number of the days of the month to which the dates are adjusted.
            The first date in the list is defined as the corresponding
            day of the month to which the start date belongs.
            Mandatory if frequency is set to 'Monthly'.
        calendars: list of str, optional
            Calendars to determine the working days and national holidays for particular countries.
            Optional if currencies is provided.
        currencies: list of str, optional
            Currencies to use for calculation of the date for the working day or weekend.
            Optional if calendars is provided.
        day_of_week : DayOfWeek or str, optional
            The day of week to which dates are adjusted.
            The first date in the list is defined as
            corresponding day of week following the start date.
            The last date in the list is defined as
            corresponding day of week preceding the end date.
        count : int, optional
            The number of dates from the start date to retrieve.
            Mandatory if end_date is not specified.

    Returns
    -------
    List[np.datetime64]
        List of np.datetime64 dates.

    Examples
    --------
    >>> import datetime
    >>> import refinitiv.data as rd
    >>> from refinitiv.data import dates_and_calendars
    >>>
    >>> rd.open_session("platform.default")
    >>>
    >>> dates = rd.dates_and_calendars.date_schedule(
    ...    start_date=datetime.date(2019, 4, 30),
    ...    count=10,
    ...    frequency=dates_and_calendars.DateScheduleFrequency.WEEKLY,
    ...    calendars=["EMU", "GER"],
    ...    day_of_week="Tuesday",
    >>>)
    """

    response = Definition(
        frequency=frequency,
        start_date=start_date,
        end_date=end_date,
        calendar_day_of_month=calendar_day_of_month,
        calendars=calendars,
        currencies=currencies,
        day_of_week=day_of_week,
        count=count,
    ).get_data()

    return response.data.dates
