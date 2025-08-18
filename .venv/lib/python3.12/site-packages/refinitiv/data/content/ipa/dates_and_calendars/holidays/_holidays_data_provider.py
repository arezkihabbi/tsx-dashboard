from dataclasses import dataclass
from typing import List

import pandas as pd
from dateutil import parser
from pandas.tseries.holiday import Holiday as PandasHoliday, nearest_workday

from .._content_data_validator import ContentDataValidator
from .._request_factory import DatesAndCalendarsRequestFactory
from .._response_factory import DatesAndCalendarsResponseFactory
from ...._content_data import Data
from ...._content_data_provider import ContentDataProvider
from ....._tools import add_periods_datetime_adapter, create_repr
from ....._types import OptDateTime
from .....delivery._data._data_provider import ValidatorContainer


@dataclass
class HolidayName:
    name: str
    calendars: list
    countries: list


def holiday_name_from_dict(datum: dict):
    return HolidayName(
        name=datum["name"],
        calendars=datum["calendars"],
        countries=datum["countries"],
    )


class Holiday(PandasHoliday):
    _holiday_names = None

    def __init__(
        self,
        date: "OptDateTime" = None,
        name: str = None,
        holiday: dict = None,
        tag: str = "",
    ):
        self._holiday = holiday or {}

        if self._holiday.get("names"):
            name = self._holiday.get("names")[0]["name"]
        elif not name:
            name = "Name not requested"

        if date is not None:
            date = add_periods_datetime_adapter.get_str(date)
        else:
            date = self._holiday.get("date")

        year, month, day = pd.NA, pd.NA, pd.NA
        if date:
            _date = parser.parse(date)
            year, month, day = _date.year, _date.month, _date.day

        PandasHoliday.__init__(
            self,
            name=name,
            year=year,
            month=month,
            day=day,
            observance=nearest_workday,
        )

        self._date = date or self._holiday.get("date", "Date not requested")
        self._tag = tag
        self._countries = self._holiday.get("countries", [])
        self._calendars = self._holiday.get("calendars", [])

    @property
    def date(self):
        return self._date

    @property
    def countries(self):
        return self._countries

    @property
    def calendars(self):
        return self._calendars

    @property
    def names(self) -> List[HolidayName]:
        if self._holiday_names is None:
            self._holiday_names = [
                holiday_name_from_dict(holiday_name) for holiday_name in self._holiday.get("names", [])
            ]
        return self._holiday_names

    @property
    def tag(self):
        return self._tag

    def __repr__(self):
        return create_repr(self, class_name="HolidayData", content="representation of 'holidayOutputs' response")


@dataclass
class HolidaysData(Data):
    _holidays: List[Holiday] = None

    @property
    def holidays(self) -> List[Holiday]:
        if self._holidays is None:
            self._holidays = [
                Holiday(holiday=holiday, tag=raw_item.get("tag"))
                for raw_item in self.raw
                if not raw_item.get("error")
                for holiday in raw_item["holidays"]
            ]

        return self._holidays


holidays_data_provider = ContentDataProvider(
    request=DatesAndCalendarsRequestFactory(),
    response=DatesAndCalendarsResponseFactory(data_class=HolidaysData),
    validator=ValidatorContainer(content_validator=ContentDataValidator()),
)
