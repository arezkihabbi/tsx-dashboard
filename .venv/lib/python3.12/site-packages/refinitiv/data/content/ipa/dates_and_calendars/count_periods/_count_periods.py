from datetime import datetime, timedelta
from typing import List, Optional, Union, TYPE_CHECKING

from numpy import iterable

from ._count_periods_data_provider import CountedPeriod, CountedPeriods
from .._base_request_items import StartEndDateBase
from ..._enums import DayCountBasis, PeriodType
from ...._content_provider_layer import ContentUsageLoggerMixin
from ....._content_type import ContentType
from ....._tools import create_repr, try_copy_to_list
from .....delivery._data._data_provider import DataProviderLayer, Response

if TYPE_CHECKING:
    from ....._types import ExtendedParams, OptDateTime, OptStrStrs


class CountPeriodsRequestItem(StartEndDateBase):
    def __init__(
        self,
        tag: Optional[str],
        start_date: Union[str, datetime, timedelta],
        end_date: Union[str, datetime, timedelta],
        period_type: Optional[PeriodType],
        calendars: Optional[List[str]],
        currencies: Optional[List[str]],
        day_count_basis,
    ):
        super().__init__(start_date, end_date)
        self.tag = tag
        self.calendars = calendars
        self.period_type = period_type
        self.currencies = currencies
        self.day_count_basis = day_count_basis

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
        """
        :return: list
        """
        self._set_parameter("calendars", value)

    @property
    def period_type(self):
        """
        :return: PeriodType
        """
        return self._get_enum_parameter(PeriodType, "periodType")

    @period_type.setter
    def period_type(self, value):
        self._set_enum_parameter(PeriodType, "periodType", value)

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
    def day_count_basis(self):
        """
        :return: DayCountBasis
        """
        return self._get_enum_parameter(DayCountBasis, "dayCountBasis")

    @day_count_basis.setter
    def day_count_basis(self, value):
        self._set_enum_parameter(DayCountBasis, "dayCountBasis", value)


class Definition(
    ContentUsageLoggerMixin[Response[CountedPeriod]],
    DataProviderLayer[Response[CountedPeriod]],
):
    """
    Count periods definition object

    Parameters
    ----------
        start_date: str or datetime or timedelta
            Start date of calculation.
        end_date: str or datetime or timedelta
            End date of calculation.
        tag: str, optional
            Reference tag to map particular response in payload.
        period_type : PeriodType or str, optional
            The method we chose to count the period of time based on value from PeriodType enumeration.
        calendars: list of str, optional
            Calendars to use the date for working day or weekend.
            Optional if currencies is provided.
        currencies: list of str, optional
            Currencies to use the date for working day or weekend.
            Optional if calendars is provided.
        day_count_basis: DayCountBasis or str, optional
            Day count basis value from DayCountBasis enumeration.
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
    >>> from refinitiv.data.content.ipa.dates_and_calendars import count_periods
    >>> definition = count_periods.Definition(
    ...   tag="my request",
    ...   start_date=datetime.timedelta(-11),
    ...   end_date=datetime.timedelta(-3),
    ...   period_type=count_periods.PeriodType.WORKING_DAY,
    ...   calendars=["EMU"],
    ...   currencies=["EUR"],
    ...   day_count_basis=count_periods.DayCountBasis.DCB_30_360
    ... )
    >>> response = definition.get_data()

    Using get_data_async

    >>> import asyncio
    >>> task = definition.get_data_async()
    >>> response = asyncio.run(task)
    """

    _USAGE_CLS_NAME = "IPA.DatesAndCalendars.CountPeriodsDefinition"

    def __init__(
        self,
        start_date: "OptDateTime" = None,
        end_date: "OptDateTime" = None,
        tag: Optional[str] = None,
        period_type: Optional[Union[PeriodType, str]] = None,
        calendars: "OptStrStrs" = None,
        currencies: "OptStrStrs" = None,
        day_count_basis: Optional[Union[DayCountBasis, str]] = None,
        extended_params: "ExtendedParams" = None,
    ):
        calendars = try_copy_to_list(calendars)
        currencies = try_copy_to_list(currencies)
        self.extended_params = extended_params

        self.request_item = CountPeriodsRequestItem(
            tag=tag,
            start_date=start_date,
            end_date=end_date,
            period_type=period_type,
            calendars=calendars,
            currencies=currencies,
            day_count_basis=day_count_basis,
        )

        super().__init__(
            data_type=ContentType.DATES_AND_CALENDARS_COUNT_PERIODS,
            universe=[self.request_item],
            extended_params=extended_params,
        )

    def __repr__(self):
        return create_repr(self)


DefnDefns = Union[List[Definition], Definition]


class Definitions(
    ContentUsageLoggerMixin[Response[CountedPeriods]],
    DataProviderLayer[Response[CountedPeriods]],
):
    """
    Count periods definitions object

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
    >>> from refinitiv.data.content.ipa.dates_and_calendars import count_periods
    >>> first_definition = count_periods.Definition(
    ...   tag="my request",
    ...   start_date=datetime.timedelta(-11),
    ...   end_date=datetime.timedelta(-3),
    ...   period_type=count_periods.PeriodType.WORKING_DAY,
    ...   calendars=["EMU"],
    ...   currencies=["EUR"],
    ...   day_count_basis=count_periods.DayCountBasis.DCB_30_360
    ... )
    ...
    >>> second_definition = count_periods.Definition(
    ...   tag="my second request",
    ...   start_date=datetime.timedelta(-15),
    ...   end_date=datetime.timedelta(-10),
    ...   period_type=count_periods.PeriodType.NON_WORKING_DAY,
    ...   calendars=["EMU"],
    ...   currencies=["EUR"],
    ...   day_count_basis=count_periods.DayCountBasis.DCB_30_360
    ... )
    >>> response = count_periods.Definitions([first_definition, second_definition]).get_data()

    Using get_data_async

    >>> import asyncio
    >>> task = count_periods.Definitions([first_definition, second_definition]).get_data_async()
    >>> response = asyncio.run(task)
    """

    _USAGE_CLS_NAME = "IPA.DatesAndCalendars.CountPeriodsDefinitions"

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
            data_type=ContentType.DATES_AND_CALENDARS_COUNT_PERIODS,
            universe=request_items,
            extended_params=extended_params,
        )

    def __repr__(self):
        return create_repr(self)
