from typing import Union, TYPE_CHECKING
from urllib.parse import quote_plus

from ._historical_pricing_request_factory import get_content_type_by_interval
from .._content_data import Data
from .._intervals import DayIntervalType, Intervals, get_day_interval_type
from ..._tools import hp_universe_parser, validate_types, try_copy_to_list, hp_datetime_adapter
from ...delivery._data._data_provider import Response, DataProviderLayer

if TYPE_CHECKING:
    from ._enums import OptAdjustments, OptMarketSession
    from ..._types import (
        OptInt,
        ExtendedParams,
        OptDateTime,
        StrStrings,
        StrStrings,
    )


class Definition(DataProviderLayer[Response[Data]]):
    """
    Creates a definition containing a summary of the specified historical pricing events.

    Parameters
    ----------
    universe : str or list of str
        Single instrument or list of instruments.
    interval : str or Intervals, optional
        Predefined interval for filtering historical pricing events.
    start : str or date or datetime or timedelta, optional
        Start time for the events query.
    end : str or date or datetime or timedelta, optional
        End time for the events query.
    adjustments : list of Adjustments or Adjustments or str, optional
        Single adjustment type or list of adjustment types to apply CORAX (Corporate Actions) events or exchange/manual
        corrections to the historical time series data.
    sessions : list of MarketSession or MarketSession or str, optional
        Market session durations, such as pre-market session, normal market session and post-market session.
    count : int, optional
        The maximum number of rows to return.
    fields : list, optional
        The list of fields to return.
    extended_params : dict, optional
        Additional parameters to apply to the request.

    Examples
    --------
    >>> from refinitiv.data.content.historical_pricing import summaries
    >>> definition_summaries = summaries.Definition("EUR")
    >>> response = definition_summaries.get_data()

    """

    def __init__(
        self,
        universe: "StrStrings",
        interval: Union[str, Intervals] = None,
        start: "OptDateTime" = None,
        end: "OptDateTime" = None,
        adjustments: "OptAdjustments" = None,
        sessions: "OptMarketSession" = None,
        count: "OptInt" = None,
        fields: "StrStrings" = None,
        extended_params: "ExtendedParams" = None,
    ) -> None:
        start = hp_datetime_adapter.get_localize(start)
        end = hp_datetime_adapter.get_localize(end)
        # By default, if interval is not defined, interday default value is requested
        day_interval_type = get_day_interval_type(interval or DayIntervalType.INTER)
        content_type = get_content_type_by_interval(day_interval_type)
        validate_types(count, [int, type(None)], "count")
        universe = try_copy_to_list(universe)
        universe = hp_universe_parser.get_list(universe)
        universe = list(map(lambda item: "/" in item and quote_plus(item) or item, universe))
        adjustments = try_copy_to_list(adjustments)
        sessions = try_copy_to_list(sessions)
        fields = try_copy_to_list(fields)

        super().__init__(
            data_type=content_type,
            universe=universe,
            interval=interval,
            start=start,
            end=end,
            adjustments=adjustments,
            sessions=sessions,
            count=count,
            fields=fields,
            extended_params=extended_params,
        )
