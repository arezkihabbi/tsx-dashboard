from dataclasses import dataclass
from typing import List

import numpy as np

from .._content_data_validator import ContentDataValidator
from .._request_factory import DateScheduleRequestFactory
from .._response_factory import DatesAndCalendarsResponseFactory
from ...._content_data import Data
from ...._content_data_provider import ContentDataProvider
from .....delivery._data._data_provider import ValidatorContainer


@dataclass
class DateSchedule(Data):
    _dates: List[np.datetime64] = None

    @property
    def dates(self):
        if self._dates is None:
            self._dates = [np.datetime64(date) for date in self.raw["dates"]]

        return self._dates


date_schedule_data_provider = ContentDataProvider(
    request=DateScheduleRequestFactory(),
    response=DatesAndCalendarsResponseFactory(data_class=DateSchedule),
    validator=ValidatorContainer(content_validator=ContentDataValidator()),
)
