from typing import Optional, Union, TYPE_CHECKING

from ._date_schedule_data_provider import DateSchedule
from .._base_request_items import StartEndDateBase
from ...._content_provider_layer import ContentUsageLoggerMixin

from ..._enums import DateScheduleFrequency, DayOfWeek
from ....._content_type import ContentType
from ....._tools import create_repr, try_copy_to_list
from .....delivery._data._data_provider import DataProviderLayer, Response

if TYPE_CHECKING:
    from ....._types import ExtendedParams, OptInt, OptDateTime, OptStrStrs


class DateScheduleRequestItem(StartEndDateBase):
    def __init__(
        self,
        start_date,
        end_date,
        count,
        frequency,
        calendars,
        currencies,
        day_of_week,
        calendar_day_of_month,
    ):
        super().__init__(start_date, end_date)
        self.count = count
        self.frequency = frequency
        self.calendars = calendars
        self.currencies = currencies
        self.day_of_week = day_of_week
        self.calendar_day_of_month = calendar_day_of_month

    @property
    def count(self):
        """
        :return: int
        """
        return self._get_parameter("count")

    @count.setter
    def count(self, value):
        self._set_parameter("count", value)

    @property
    def calendars(self):
        """
        :return: list
        """
        return self._get_parameter("calendars")

    @calendars.setter
    def calendars(self, value):
        self._set_parameter("calendars", value)

    @property
    def currencies(self):
        """
        :return: list
        """
        return self._get_parameter("currencies")

    @currencies.setter
    def currencies(self, value):
        self._set_parameter("currencies", value)

    @property
    def frequency(self):
        """
        :return: DateScheduleFrequency
        """
        return self._get_enum_parameter(DateScheduleFrequency, "frequency")

    @frequency.setter
    def frequency(self, value):
        self._set_enum_parameter(DateScheduleFrequency, "frequency", value)

    @property
    def day_of_week(self):
        """
        :return: DayOfWeek
        """
        return self._get_enum_parameter(DayOfWeek, "DayOfWeek")

    @day_of_week.setter
    def day_of_week(self, value):
        self._set_enum_parameter(DayOfWeek, "DayOfWeek", value)

    @property
    def calendar_day_of_month(self):
        """
        :return: str
        """
        return self._get_parameter("calendarDayOfMonth")

    @calendar_day_of_month.setter
    def calendar_day_of_month(self, value):
        self._set_parameter("calendarDayOfMonth", value)


class Definition(
    ContentUsageLoggerMixin[Response[DateSchedule]],
    DataProviderLayer[Response[DateSchedule]],
):
    """
    Date schedule definition object

    Parameters
    ----------
        frequency: DateScheduleFrequency or str
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
            The number of the day of the month to which dates are adjusted.
            The first date in the list is defined as the corresponding
            day of the month to which the start date belongs.
            Mandatory if frequency is set to 'Monthly'.
        calendars: list of str, optional
            Calendars to use the date for working day or weekend.
            Optional if currencies is provided.
        currencies: list of str, optional
            Currencies to use the date for working day or weekend.
            Optional if calendars is provided.
        day_of_week : DayOfWeek or str, optional
            The day of week to which dates are adjusted.
            The first date in the list is defined as
            corresponding day of week following the start date.
            The last date in the list is defined as
            corresponding day of week preceding the end date.
        count : int, optional
            A number is used to define a list of dates from the
            start date (or today if the start day is not set) to the end date.
            Mandatory if end_date is not specified.
        extended_params : dict, optional
            If necessary other parameters.

    Methods
    -------
    get_data(session=None, on_response=None, **kwargs)
        Returns a response to the data platform
    get_data_async(session=None, on_response=None, **kwargs)
        Returns a response asynchronously to the data platform

    Examples
    --------
    >>> import datetime
    >>> from refinitiv.data.content.ipa.dates_and_calendars import date_schedule
    >>> definition = date_schedule.Definition(
    ...     start_date="2020-01-01",
    ...     end_date=datetime.timedelta(0),
    ...     frequency="Weekly",
    ...     calendars=["EMU", "GER"],
    ...     day_of_week=date_schedule.DayOfWeek.MONDAY,
    ... )
    >>> response = definition.get_data()

    Using get_data_async

    >>> import asyncio
    >>> task = definition.get_data_async()
    >>> response = asyncio.run(task)
    """

    _USAGE_CLS_NAME = "IPA.DatesAndCalendars.DateScheduleDefinition"

    def __init__(
        self,
        frequency: Union[DateScheduleFrequency, str, None] = None,
        start_date: "OptDateTime" = None,
        end_date: "OptDateTime" = None,
        calendar_day_of_month: "OptInt" = None,
        calendars: "OptStrStrs" = None,
        currencies: "OptStrStrs" = None,
        day_of_week: Optional[Union[DayOfWeek, str]] = None,
        count: "OptInt" = None,
        extended_params: "ExtendedParams" = None,
    ):
        calendars = try_copy_to_list(calendars)
        currencies = try_copy_to_list(currencies)
        self.request_item = DateScheduleRequestItem(
            start_date=start_date,
            end_date=end_date,
            count=count,
            frequency=frequency,
            calendars=calendars,
            currencies=currencies,
            calendar_day_of_month=calendar_day_of_month,
            day_of_week=day_of_week,
        )

        super().__init__(
            data_type=ContentType.DATES_AND_CALENDARS_DATE_SCHEDULE,
            universe=self.request_item,
            extended_params=extended_params,
        )

    def __repr__(self):
        return create_repr(self)
