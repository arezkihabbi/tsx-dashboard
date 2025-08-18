from collections import defaultdict
from dataclasses import dataclass
from typing import List, Optional, Dict

import pandas as pd
from dateutil import parser
from pandas.tseries.holiday import AbstractHolidayCalendar, nearest_workday, Holiday

from ..._types import OptDateTime
from ...content.ipa.dates_and_calendars.holidays import Definition


class HolidayCalendar(AbstractHolidayCalendar):
    """
    Custom Holiday Calendar
    """

    def __init__(self, custom_holidays: list):
        super().__init__()
        self._custom_holidays = custom_holidays

    @property
    def rules(self) -> List[Holiday]:
        # rules are compatible with pandas
        return [self._create_rule(hol["date"], hol["name"]) for hol in self._custom_holidays]

    @property
    def rules_list(self) -> List[dict]:
        # for easy access to all holidays the list of holidays is exposed
        return [self._create_holiday(hol["date"], hol["name"]) for hol in self._custom_holidays]

    @property
    def offset(self):
        return pd.offsets.CustomBusinessDay(calendar=self)

    @staticmethod
    def _create_holiday(date, name):
        date = parser.parse(date)
        return {"date": date, "name": name}

    @staticmethod
    def _create_rule(date, name, observance=None):
        # create a single rule from a holiday
        date = parser.parse(date)
        year, month, day = date.year, date.month, date.day
        observance = observance or nearest_workday
        a = Holiday(name=name, year=year, month=month, day=day, observance=observance)
        return a


def holidays_per_calendar(response) -> dict:
    def extract_holiday(holiday_info):
        return {
            "date": holiday_info.get("date"),
            "name": holiday_info.get("names")[0]["name"],
        }

    _holidays_per_calendar = defaultdict(list)
    for holiday in response:
        for cldr in holiday.get("calendars"):
            _holidays_per_calendar[cldr].append(extract_holiday(holiday))
    return _holidays_per_calendar


@dataclass
class HolidaysResponse:
    df: pd.DataFrame
    calendars: Dict[str, HolidayCalendar]
    offset: pd.offsets.CustomBusinessDay


def holidays(
    start_date: "OptDateTime" = None,
    end_date: "OptDateTime" = None,
    calendars: Optional[List[str]] = None,
    currencies: Optional[List[str]] = None,
) -> HolidaysResponse:
    """
    Gets the holidays between the start date and the end date using one or many calendars.

    Parameters
    ----------
    start_date: str or datetime or timedelta, optional
        Calculation start date.
    end_date: str or datetime or timedelta, optional
        Calculation end date.
    calendars: list of str, optional
        Calendars to determine the working days and national holidays for particular countries.
        Optional if currencies is provided.
    currencies: list of str, optional
        Currencies to use for calculation of the date for the working day or weekend.
        Optional if calendars is provided.

    Returns
    -------
    HolidaysResponse
        HolidaysResponse object with dataframe, requested calendars and offset

    Examples
    --------
    >>> import datetime
    >>> import refinitiv.data as rd
    >>>
    >>> rd.open_session("platform.default")
    >>>
    >>> holidays_response = rd.dates_and_calendars.holidays(
    >>>    start_date=datetime.datetime(2019, 11, 20),
    >>>    end_date=datetime.datetime(2020, 2, 20),
    >>>    calendars=["EMU", "GER"],
    >>>)
    """

    holiday_outputs = ["Date", "Names", "Calendars", "Countries"]

    response = Definition(
        start_date=start_date,
        end_date=end_date,
        calendars=calendars,
        currencies=currencies,
        holiday_outputs=holiday_outputs,
    ).get_data()

    _holidays_per_calendar = holidays_per_calendar(response.data.raw[0].get("holidays", []))

    holiday_calendars = {}
    for calendar, holidays_ in _holidays_per_calendar.items():
        holiday_calendars[calendar] = HolidayCalendar(holidays_)

    all_calendar_holidays = []
    for items in _holidays_per_calendar.values():
        for item in items:
            flag = True
            for holiday in all_calendar_holidays:
                if holiday["date"] == item["date"]:
                    flag = False
                    break

            if flag:
                all_calendar_holidays.append(item)

    global_holiday_calendar = HolidayCalendar(all_calendar_holidays)

    response = HolidaysResponse(response.data.df, holiday_calendars, global_holiday_calendar.offset)

    return response
