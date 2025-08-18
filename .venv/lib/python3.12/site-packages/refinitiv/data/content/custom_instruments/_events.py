from typing import TYPE_CHECKING
from urllib.parse import quote_plus

from .._content_data import Data
from .._content_provider_layer import ContentUsageLoggerMixin
from ..._content_type import ContentType
from ..._tools import custom_insts_historical_universe_parser, try_copy_to_list, custom_inst_datetime_adapter
from ...delivery._data._data_provider import DataProviderLayer, Response

if TYPE_CHECKING:
    from ..._types import OptDateTime, StrStrings, OptInt, ExtendedParams, OptStrStrs


class Definition(ContentUsageLoggerMixin[Response[Data]], DataProviderLayer[Response[Data]]):
    """
    Summary line of this class that defines parameters for requesting events from custom instruments

    Parameters
    ----------
    universe : str or list
        The Id or Symbol of custom instrument to operate on
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
    >>> from refinitiv.data.content.custom_instruments import events
    >>> definition_events = events.Definition("S)My.CustomInstrument")
    >>> response = definition_events.get_data()
    """

    _USAGE_CLS_NAME = "CustomInstruments.EventsDefinition"

    def __init__(
        self,
        universe: "StrStrings",
        start: "OptDateTime" = None,
        end: "OptDateTime" = None,
        count: "OptInt" = None,
        fields: "OptStrStrs" = None,
        extended_params: "ExtendedParams" = None,
    ):
        start = custom_inst_datetime_adapter.get_localize(start)
        end = custom_inst_datetime_adapter.get_localize(end)
        fields = try_copy_to_list(fields)
        universe = try_copy_to_list(universe)
        universe = custom_insts_historical_universe_parser.get_list(universe)
        universe = list(map(lambda item: "/" in item and quote_plus(item) or item, universe))
        super().__init__(
            data_type=ContentType.CUSTOM_INSTRUMENTS_EVENTS,
            universe=universe,
            start=start,
            end=end,
            count=count,
            fields=fields,
            extended_params=extended_params,
        )
