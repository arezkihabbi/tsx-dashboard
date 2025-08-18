from dataclasses import dataclass
from typing import Any, List, Optional

from .._content_data_validator import ContentDataValidator
from .._request_factory import DatesAndCalendarsRequestFactory
from .._response_factory import DatesAndCalendarsResponseFactory
from ..holidays._holidays_data_provider import Holiday
from ...._content_data import Data
from ...._content_data_provider import ContentDataProvider
from ...._df_builder import build_dates_calendars_df
from .....delivery._data._data_provider import ValidatorContainer


@dataclass
class WorkingDay:
    is_weekend: bool
    is_working_day: bool
    tag: str = ""
    holidays: Optional[list] = None


def working_day_from_dict(datum: dict):
    holidays = datum.get("holidays", [])
    tag = datum.get("tag")
    holidays = [Holiday(holiday=holiday, tag=tag) for holiday in holidays]

    return WorkingDay(
        is_weekend=datum["isWeekEnd"],
        is_working_day=datum.get("isWorkingDay"),
        tag=tag,
        holidays=holidays,
    )


@dataclass
class IsWorkingDay(Data):
    _day: WorkingDay = None

    @property
    def day(self):
        return self._day


@dataclass
class IsWorkingDays(Data):
    _is_working_days_: List[WorkingDay] = None

    @property
    def _is_working_days(self):
        if self._is_working_days_ is None:
            self._is_working_days_ = [
                working_day_from_dict(raw_item) for raw_item in self.raw if not raw_item.get("error")
            ]

        return self._is_working_days_

    @property
    def days(self):
        return self._is_working_days

    def __getitem__(self, item: int):
        return self._is_working_days[item]


class IsWorkingDayResponseFactory(DatesAndCalendarsResponseFactory):
    def create_data_success(self, raw: Any, **kwargs):
        if len(raw) > 1:
            data = IsWorkingDays(raw=raw, _dfbuilder=build_dates_calendars_df, _kwargs=kwargs)

        else:
            data = IsWorkingDay(
                raw=raw,
                _day=working_day_from_dict(raw[0]),
                _dfbuilder=build_dates_calendars_df,
                _kwargs=kwargs,
            )

        return data


is_working_day_data_provider = ContentDataProvider(
    request=DatesAndCalendarsRequestFactory(),
    response=IsWorkingDayResponseFactory(),
    validator=ValidatorContainer(content_validator=ContentDataValidator()),
)
