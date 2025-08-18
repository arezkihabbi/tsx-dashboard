from dataclasses import dataclass
from typing import List

from .._content_data_validator import ContentDataValidator
from .._request_factory import DatesAndCalendarsRequestFactory
from .._response_factory import DatesAndCalendarsResponseFactory
from ...._content_data import Data
from ...._content_data_provider import ContentDataProvider
from ...._df_builder import default_build_df
from .....delivery._data._data_provider import ValidatorContainer


@dataclass
class Period:
    count: float
    tenor: str
    tag: str = ""


def period_from_dict(datum: dict):
    return Period(count=datum["count"], tenor=datum["tenor"], tag=datum.get("tag"))


@dataclass
class CountedPeriods(Data):
    _counted_periods: List[Period] = None

    @property
    def counted_periods(self):
        if self._counted_periods is None:
            self._counted_periods = [period_from_dict(item) for item in self.raw]

        return self._counted_periods

    def __getitem__(self, item: int):
        return self.counted_periods[item]


@dataclass
class CountedPeriod(Data):
    _period: Period = None

    @property
    def counted_period(self):
        return self._period


class CountPeriodsResponseFactory(DatesAndCalendarsResponseFactory):
    def create_data_success(self, raw: List[dict], **kwargs):
        if len(raw) > 1:
            data = CountedPeriods(raw, _dfbuilder=default_build_df)

        else:
            data = CountedPeriod(
                raw=raw,
                _period=period_from_dict(raw[0]),
                _dfbuilder=default_build_df,
                _kwargs=kwargs,
            )

        return data


count_periods_data_provider = ContentDataProvider(
    request=DatesAndCalendarsRequestFactory(),
    response=CountPeriodsResponseFactory(),
    validator=ValidatorContainer(content_validator=ContentDataValidator()),
)
