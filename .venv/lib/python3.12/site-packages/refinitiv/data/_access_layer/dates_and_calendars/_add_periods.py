from typing import List, Optional, Union

import numpy as np

from ..._types import OptDateTime
from ...content.ipa._enums import DateMovingConvention, EndOfMonthConvention
from ...content.ipa.dates_and_calendars.add_periods import Definition


def add_periods(
    start_date: "OptDateTime" = None,
    period: str = None,
    calendars: Optional[List[str]] = None,
    currencies: Optional[List[str]] = None,
    date_moving_convention: Optional[Union[DateMovingConvention, str]] = None,
    end_of_month_convention: Optional[Union[EndOfMonthConvention, str]] = None,
) -> np.datetime64:
    """
    Retrieves the updated date, based on the provided start date and particular period of time or calendar values.

    Parameters
    ----------
        start_date: str or datetime or timedelta, optional
            Start date of calculation.
        period: str, optional
            Calculation time period.
        calendars: list of str, optional
            Calendars to determine the working days and national holidays for particular countries.
            Optional if currencies is provided.
        currencies: list of str, optional
            Currencies to use for calculation of the date for the working day or weekend.
            Optional if calendars is provided.
        date_moving_convention : DateMovingConvention or str, optional
            Convention for adjusting the dates.
        end_of_month_convention : EndOfMonthConvention or str, optional
            Possible values for the end of month.

    Returns
    -------
    np.datetime64
        Added period date

    Examples
    --------
    >>> import datetime
    >>> import refinitiv.data as rd
    >>> from refinitiv.data import dates_and_calendars
    >>>
    >>> rd.open_session("platform.default")
    >>>
    >>> added_period = rd.dates_and_calendars.add_periods(
    ...    start_date=datetime.date(2014, 1, 1),
    ...    period="1Y",
    ...    calendars=["BAR", "KOR"],
    ...    date_moving_convention=dates_and_calendars.DateMovingConvention.NEXT_BUSINESS_DAY,
    ...    end_of_month_convention=dates_and_calendars.EndOfMonthConvention.LAST28
    ... )
    """

    response = Definition(
        start_date=start_date,
        period=period,
        calendars=calendars,
        currencies=currencies,
        date_moving_convention=date_moving_convention,
        end_of_month_convention=end_of_month_convention,
    ).get_data()

    return np.datetime64(response.data.added_period.date)
