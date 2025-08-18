from typing import TYPE_CHECKING
from urllib.parse import quote_plus

from .._content_data import Data
from .._content_provider_layer import ContentUsageLoggerMixin
from ..._content_type import ContentType
from ..._tools import hp_universe_parser, validate_types, try_copy_to_list, hp_datetime_adapter
from ...delivery._data._data_provider import Response, DataProviderLayer

if TYPE_CHECKING:
    from ._enums import OptAdjustments, OptEventTypes
    from ..._types import OptDateTime, StrStrings, OptInt, ExtendedParams, OptStrStrs


class Definition(ContentUsageLoggerMixin[Response[Data]], DataProviderLayer[Response[Data]]):
    """
    Defines the Historical Pricing Events to be retrieved.

    Parameters
    ----------
    universe : str or list of str
        Single instrument or list of instruments.
    eventTypes : list of EventTypes or EventTypes or str, optional
        Single market event or list of events.
    start : str or date or datetime or timedelta, optional
        Start time for the events query.
    end : str or date or datetime or timedelta, optional
        End time for the events query.
    adjustments : list of Adjustments or Adjustments or str, optional
        Single adjustment type or list of adjustment types to apply CORAX (Corporate Actions) events or
        exchange/manual corrections to the historical time series data.
    count : int, optional
        The maximum number of rows to return.
    fields : list, optional
        List of fields to return.
    extended_params : dict, optional
        Additional parameters to apply to the request.

    Examples
    --------
    >>> from refinitiv.data.content.historical_pricing import events
    >>> definition_events = events.Definition("EUR")
    >>> response = definition_events.get_data()

    """

    _USAGE_CLS_NAME = "HistoricalPricing.EventsDefinition"

    def __init__(
        self,
        universe: "StrStrings",
        eventTypes: "OptEventTypes" = None,
        start: "OptDateTime" = None,
        end: "OptDateTime" = None,
        adjustments: "OptAdjustments" = None,
        count: "OptInt" = None,
        fields: "OptStrStrs" = None,
        extended_params: "ExtendedParams" = None,
    ):
        start = hp_datetime_adapter.get_localize(start)
        end = hp_datetime_adapter.get_localize(end)
        validate_types(count, [int, type(None)], "count")
        universe = try_copy_to_list(universe)
        universe = hp_universe_parser.get_list(universe)
        universe = list(map(lambda item: "/" in item and quote_plus(item) or item, universe))
        event_types = try_copy_to_list(eventTypes)
        adjustments = try_copy_to_list(adjustments)
        fields = try_copy_to_list(fields)

        super().__init__(
            data_type=ContentType.HISTORICAL_PRICING_EVENTS,
            universe=universe,
            event_types=event_types,
            start=start,
            end=end,
            adjustments=adjustments,
            count=count,
            fields=fields,
            extended_params=extended_params,
        )
