from typing import Union, TYPE_CHECKING
from urllib.parse import quote_plus

from ._custom_instruments_data_provider import get_content_type_by_interval
from .._content_data import Data
from .._content_provider_layer import ContentUsageLoggerMixin
from .._intervals import DayIntervalType, get_day_interval_type, Intervals
from ..._tools import (
    validate_types,
    custom_insts_historical_universe_parser,
    try_copy_to_list,
    custom_inst_datetime_adapter,
)
from ...delivery._data._data_provider import DataProviderLayer, Response

if TYPE_CHECKING:
    from ..._types import StrStrings, OptDateTime, OptInt, ExtendedParams


class Definition(ContentUsageLoggerMixin[Response[Data]], DataProviderLayer[Response[Data]]):
    """
    Summary line of this class that defines parameters for requesting summaries from custom instruments

    Parameters
    ----------
    universe : str or list
        The Id or Symbol of custom instrument to operate on
    interval : str or Intervals, optional
        The consolidation interval in ISO8601
    start : str or date or datetime or timedelta, optional
        The start date and timestamp of the query in ISO8601 with UTC only
    end : str or date or datetime or timedelta, optional
        The end date and timestamp of the query in ISO8601 with UTC only
    count : int, optional
        The maximum number of data returned. Values range: 1 - 10000
    fields : list, optional
        The list of fields that are to be returned in the response
    extended_params : dict, optional
        If necessary other parameters

    Examples
    --------
    >>> from refinitiv.data.content.custom_instruments import summaries
    >>> definition_summaries = summaries.Definition("S)My.CustomInstrument")
    >>> response = definition_summaries.get_data()
    """

    _USAGE_CLS_NAME = "CustomInstruments.SummariesDefinition"

    def __init__(
        self,
        universe: "StrStrings",
        interval: Union[str, Intervals] = None,
        start: "OptDateTime" = None,
        end: "OptDateTime" = None,
        count: "OptInt" = None,
        fields: "StrStrings" = None,
        extended_params: "ExtendedParams" = None,
    ) -> None:
        start = custom_inst_datetime_adapter.get_localize(start)
        end = custom_inst_datetime_adapter.get_localize(end)
        day_interval_type = get_day_interval_type(interval or DayIntervalType.INTER)
        content_type = get_content_type_by_interval(day_interval_type)
        validate_types(count, [int, type(None)], "count")

        fields = try_copy_to_list(fields)
        universe = try_copy_to_list(universe)
        universe = custom_insts_historical_universe_parser.get_list(universe)
        universe = list(map(lambda item: "/" in item and quote_plus(item) or item, universe))

        super().__init__(
            data_type=content_type,
            universe=universe,
            interval=interval,
            start=start,
            end=end,
            count=count,
            fields=fields,
            extended_params=extended_params,
        )
