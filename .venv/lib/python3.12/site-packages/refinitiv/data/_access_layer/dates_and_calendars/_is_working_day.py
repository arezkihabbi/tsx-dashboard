from typing import List, Optional

from ..._types import OptDateTime
from ...content.ipa.dates_and_calendars.is_working_day import Definition


def is_working_day(
    date: "OptDateTime" = None,
    currencies: Optional[List[str]] = None,
    calendars: Optional[List[str]] = None,
) -> bool:
    """
    Checks if the date is a working day or not for any of the calendars or currencies provided.

    Parameters
    ----------
        date: str or datetime or timedelta, optional
            Particular date to check.
        calendars: list of str, optional
            Calendars to use the date for the working day or weekend.
            Optional if currencies is provided.
        currencies: list of str, optional
            Currencies to use for calculation of the date for the working day or weekend.
            Optional if calendars is provided.

    Returns
    -------
    bool
        If requested day is working day returns True, otherwise returns False

    Examples
    --------
    >>> import datetime
    >>> import refinitiv.data as rd
    >>>
    >>> rd.open_session("platform.default")
    >>>
    >>> is_working = rd.dates_and_calendars.is_working_day(
    ...    date=datetime.datetime(2020, 7, 10),
    ...    currencies=["EUR"]
    >>>)
    """

    response = Definition(date=date, calendars=calendars, currencies=currencies).get_data()

    return response.data.day.is_working_day
