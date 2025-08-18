from typing import List, Optional, Union, TYPE_CHECKING

from numpy import iterable

from ._is_working_day_data_provider import IsWorkingDay, IsWorkingDays
from .._base_request_items import DateBase
from ..._enums import HolidayOutputs
from ...._content_provider_layer import ContentUsageLoggerMixin
from ....._content_type import ContentType
from ....._tools import create_repr, try_copy_to_list
from .....delivery._data._data_provider import DataProviderLayer, Response

if TYPE_CHECKING:
    from ....._types import ExtendedParams, OptStr, OptDateTime, OptStrStrs


class IsWorkingDayRequestItem(DateBase):
    def __init__(self, tag, date, calendars, currencies, holiday_outputs):
        super().__init__(date)
        self.tag = tag
        self.currencies = currencies
        self.calendars = calendars
        self.holiday_outputs = holiday_outputs

    @property
    def tag(self):
        """
        :return: str
        """
        return self._get_parameter("tag")

    @tag.setter
    def tag(self, value):
        self._set_parameter("tag", value)

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
    def calendars(self):
        """
        :return: list
        """
        return self._get_parameter("calendars")

    @calendars.setter
    def calendars(self, value):
        self._set_parameter("calendars", value)

    @property
    def holiday_outputs(self):
        """
        :return: list
        """
        return self._get_list_of_enums(HolidayOutputs, "holidayOutputs")

    @holiday_outputs.setter
    def holiday_outputs(self, value):
        self._set_list_of_enums(HolidayOutputs, "holidayOutputs", value)


class Definition(
    ContentUsageLoggerMixin[Response[IsWorkingDay]],
    DataProviderLayer[Response[IsWorkingDay]],
):
    """
    Is working day definition object

    Parameters
    ----------
        date: str or datetime or timedelta
            Date to test.
        calendars: list of str, optional
            Calendars to use the date for working day or weekend.
            Optional if currencies is provided.
        currencies: list of str, optional
            Currencies to use the date for working day or weekend.
            Optional if calendars is provided.
        holiday_outputs : HolidayOutputs or list of str, optional
            In case if test date is holiday you may request additional information about the holiday.
            Possible options are: Date, Names, Calendars, Countries
        tag: str, optional
            Reference tag to map particular response in payload.
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
    >>> from refinitiv.data.content.ipa.dates_and_calendars import is_working_day
    >>>
    >>> definition = is_working_day.Definition(
    ...   tag="my request",
    ...   date=datetime.timedelta(0),
    ...   currencies=["EUR"],
    ...   holiday_outputs=["Date", "Names", "Calendars", "Countries"]
    ... )
    >>> response = definition.get_data()

    Using get_data_async

    >>> import asyncio
    >>> task = definition.get_data_async()
    >>> response = asyncio.run(task)
    """

    _USAGE_CLS_NAME = "IPA.DatesAndCalendars.IsWorkingDayDefinition"

    def __init__(
        self,
        date: "OptDateTime" = None,
        currencies: "OptStrStrs" = None,
        calendars: "OptStrStrs" = None,
        holiday_outputs: Optional[Union[List[HolidayOutputs], List[str]]] = None,
        tag: "OptStr" = None,
        extended_params: "ExtendedParams" = None,
    ):
        currencies = try_copy_to_list(currencies)
        calendars = try_copy_to_list(calendars)
        holiday_outputs = try_copy_to_list(holiday_outputs)
        self.extended_params = extended_params

        self.request_item = IsWorkingDayRequestItem(
            tag=tag,
            date=date,
            calendars=calendars,
            currencies=currencies,
            holiday_outputs=holiday_outputs,
        )

        super().__init__(
            data_type=ContentType.DATES_AND_CALENDARS_IS_WORKING_DAY,
            universe=[self.request_item],
            extended_params=extended_params,
        )

    def __repr__(self):
        return create_repr(self)


DefnDefns = Union[List[Definition], Definition]


class Definitions(
    ContentUsageLoggerMixin[Response[IsWorkingDays]],
    DataProviderLayer[Response[IsWorkingDays]],
):
    """
    Is working day definitions object

    Parameters
    ----------
    universe: Definition or list of Definition objects
        List of initialized Definition objects to retrieve data.

    Methods
    -------
    get_data(session=None, on_response=None, **kwargs)
        Returns a response to the data platform
    get_data_async(session=None, on_response=None, **kwargs)
        Returns a response asynchronously to the data platform

    Examples
    --------
    >>> import datetime
    >>> from refinitiv.data.content.ipa.dates_and_calendars import is_working_day
    >>>
    >>> first_definition = is_working_day.Definition(
    ...   tag="my request",
    ...   date=datetime.timedelta(0),
    ...   currencies=["EUR"],
    ...   holiday_outputs=["Date", "Names", "Calendars", "Countries"]
    ... )
    ...
    >>>
    >>> second_definition = is_working_day.Definition(
    ...   tag="my second request",
    ...   date="2020-01-01",
    ...   currencies=["EUR"],
    ...   holiday_outputs=["Date", "Names", "Calendars", "Countries"]
    ... )
    >>> response = is_working_day.Definitions([first_definition, second_definition]).get_data()

    Using get_data_async

    >>> import asyncio
    >>> task = is_working_day.Definitions([first_definition, second_definition]).get_data_async()
    >>> response = asyncio.run(task)
    """

    _USAGE_CLS_NAME = "IPA.DatesAndCalendars.IsWorkingDayDefinitions"

    def __init__(self, universe: "DefnDefns"):
        universe = try_copy_to_list(universe)
        if not iterable(universe):
            universe = [universe]

        request_items = []
        extended_params = []
        for item in universe:
            request_items.append(item.request_item)
            extended_params.append(item.extended_params)

        super().__init__(
            data_type=ContentType.DATES_AND_CALENDARS_IS_WORKING_DAY,
            universe=request_items,
            extended_params=extended_params,
        )

    def __repr__(self):
        return create_repr(self)
