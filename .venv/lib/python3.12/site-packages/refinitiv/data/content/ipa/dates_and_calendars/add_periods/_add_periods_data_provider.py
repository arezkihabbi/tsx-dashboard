from dataclasses import dataclass
from typing import List, Union

from .._content_data_validator import ContentDataValidator
from .._request_factory import DatesAndCalendarsRequestFactory
from .._response_factory import DatesAndCalendarsResponseFactory
from ..holidays._holidays_data_provider import Holiday
from ...._content_data import Data
from ...._content_data_provider import ContentDataProvider
from ...._df_builder import build_dates_calendars_df
from .....delivery._data._data_provider import ValidatorContainer


@dataclass
class Period:
    date: str
    holidays: Union[list, None]
    tag: str = ""


def period_from_dict(datum: dict):
    tag = datum.get("tag")
    holidays = datum.get("holidays", [])
    holidays = [Holiday(holiday=holiday, tag=tag) for holiday in holidays]

    return Period(date=datum["date"], holidays=holidays, tag=tag)


@dataclass
class AddedPeriods(Data):
    _added_periods: List = None

    @property
    def added_periods(self):
        if self._added_periods is None:
            self._added_periods = [period_from_dict(raw_item) for raw_item in self.raw if not raw_item.get("error")]

        return self._added_periods

    def __getitem__(self, item):
        return self.added_periods[item]


@dataclass
class AddedPeriod(Data):
    _period: Period = None

    @property
    def added_period(self):
        return self._period


class AddPeriodsResponseFactory(DatesAndCalendarsResponseFactory):
    def create_data_success(self, raw: List[dict], **kwargs):
        if len(raw) > 1:
            data = AddedPeriods(raw, _dfbuilder=build_dates_calendars_df)

        else:
            raw_item = raw[0]
            data = AddedPeriod(
                raw=raw,
                _period=period_from_dict(raw_item),
                _dfbuilder=build_dates_calendars_df,
            )

        return data


add_period_data_provider = ContentDataProvider(
    request=DatesAndCalendarsRequestFactory(),
    response=AddPeriodsResponseFactory(),
    validator=ValidatorContainer(content_validator=ContentDataValidator()),
)
