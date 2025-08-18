from typing import List, Optional, Union, TYPE_CHECKING

from numpy import iterable

from ._holidays_data_provider import HolidaysData
from .._base_request_items import StartEndDateBase
from ..._enums import HolidayOutputs
from ...._content_provider_layer import ContentUsageLoggerMixin
from ....._content_type import ContentType
from ....._tools import create_repr, try_copy_to_list
from .....delivery._data._data_provider import DataProviderLayer, Response

if TYPE_CHECKING:
    from ....._types import ExtendedParams, OptStr, OptDateTime, OptStrStrs


class HolidaysRequestItem(StartEndDateBase):
    def __init__(self, tag, start_date, end_date, calendars, currencies, holiday_outputs):
        super().__init__(start_date, end_date)
        self.tag = tag
        self.calendars = calendars
        self.currencies = currencies
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
    def holiday_outputs(self):
        """
        :return: list
        """
        return self._get_list_of_enums(HolidayOutputs, "holidayOutputs")

    @holiday_outputs.setter
    def holiday_outputs(self, value):
        self._set_list_of_enums(HolidayOutputs, "holidayOutputs", value)


class Definition(
    ContentUsageLoggerMixin[Response[HolidaysData]],
    DataProviderLayer[Response[HolidaysData]],
):
    """
    Holidays definition object

    Parameters
    ----------
    start_date: str or datetime or timedelta
        Start date of calculation.
    end_date: str or datetime or timedelta
        End date of calculation.
    tag: str, optional
        Reference tag to map particular response in payload.
    calendars: list of str, optional
        Calendars to use the date for working day or weekend.
        Optional if currencies is provided.
    currencies: list of str, optional
        Currencies to use the date for working day or weekend.
        Optional if calendars is provided.
    holiday_outputs : HolidayOutputs or list of str, optional
        In case if test date is holiday you may request additional information about the holiday.
        Possible options are: Date, Names, Calendars, Countries
    extended_params : dict, optional
        If necessary other parameters.

    Methods
    -------
    get_data(session=None, on_response=None, **kwargs)
        Returns a response to the data platform.
    get_data_async(session=None, on_response=None, **kwargs)
        Returns a response asynchronously to the data platform.

    Examples
    --------
    >>> import datetime
    >>> from refinitiv.data.content.ipa.dates_and_calendars import holidays
    >>>
    >>> definition = holidays.Definition(
    ...   tag="my request",
    ...   start_date=datetime.datetime(2020, 5, 2),
    ...   end_date=datetime.timedelta(-30),
    ...   calendars=["UKR", "FRA"],
    ...   currencies=["EUR"],
    ...   holiday_outputs=["Date", "Names", "Calendars", "Countries"]
    ... )
    >>> response = definition.get_data()

    Using get_data_async

    >>> import asyncio
    >>> task = definition.get_data_async()
    >>> response = asyncio.run(task)
    """

    _USAGE_CLS_NAME = "IPA.DatesAndCalendars.HolidaysDefinition"

    def __init__(
        self,
        start_date: "OptDateTime" = None,
        end_date: "OptDateTime" = None,
        tag: "OptStr" = None,
        calendars: "OptStrStrs" = None,
        currencies: "OptStrStrs" = None,
        holiday_outputs: Optional[Union[List[HolidayOutputs], List[str]]] = None,
        extended_params: "ExtendedParams" = None,
    ):
        calendars = try_copy_to_list(calendars)
        currencies = try_copy_to_list(currencies)
        holiday_outputs = try_copy_to_list(holiday_outputs)
        self.extended_params = extended_params

        self.request_item = HolidaysRequestItem(
            tag=tag,
            start_date=start_date,
            end_date=end_date,
            calendars=calendars,
            currencies=currencies,
            holiday_outputs=holiday_outputs,
        )

        super().__init__(
            data_type=ContentType.DATES_AND_CALENDARS_HOLIDAYS,
            universe=[self.request_item],
            extended_params=extended_params,
        )

    def __repr__(self):
        return create_repr(self)


DefnDefns = Union[List[Definition], Definition]


class Definitions(
    ContentUsageLoggerMixin[Response[HolidaysData]],
    DataProviderLayer[Response[HolidaysData]],
):
    """
    Holidays definitions object

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
    >>> from refinitiv.data.content.ipa.dates_and_calendars import holidays
    >>>
    >>> first_definition = holidays.Definition(
    ...   tag="my request",
    ...   start_date=datetime.datetime(2020, 5, 2),
    ...   end_date=datetime.timedelta(-30),
    ...   calendars=["UKR", "FRA"],
    ...   currencies=["EUR"],
    ...   holiday_outputs=["Date", "Names", "Calendars", "Countries"]
    ... )
    ...
    >>>
    >>> second_definition = holidays.Definition(
    ...   tag="my second request",
    ...   start_date="2020-01-01",
    ...   end_date=datetime.timedelta(0),
    ...   calendars=["UKR", "FRA"],
    ...   currencies=["EUR"],
    ...   holiday_outputs=["Date", "Names", "Calendars", "Countries"]
    ... )
    >>> response = holidays.Definitions([first_definition, second_definition]).get_data()

    Using get_data_async

    >>> import asyncio
    >>> task = holidays.Definitions([first_definition, second_definition]).get_data_async()
    >>> response = asyncio.run(task)
    """

    _USAGE_CLS_NAME = "IPA.DatesAndCalendars.HolidaysDefinitions"

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
            data_type=ContentType.DATES_AND_CALENDARS_HOLIDAYS,
            universe=request_items,
            extended_params=extended_params,
        )

    def __repr__(self):
        return create_repr(self)
