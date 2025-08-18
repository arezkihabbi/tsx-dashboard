"""Access layer.

Access layer provides a set of simplified interfaces offering coders uniform access to the breadth and depth of
financial data and services available on the Refinitiv Data Platform. The platform refers to the layer of data
services providing streaming and non-streaming content, bulk content and even more, serving different client types
from the simple desktop interface to the enterprise application.
"""

from typing import TYPE_CHECKING as _TYPE_CHECKING

if _TYPE_CHECKING:
    import dates_and_calendars
    from .get_data_func import get_data
    from .get_history_func import get_history
    from .get_stream import open_pricing_stream, PricingStream
    import news
    from .session import close_session, open_session

from .._tools import lazy_attach

_submodules = {"dates_and_calendars", "news"}

_submod_attrs = {
    "dates_and_calendars": [
        "add_periods",
        "count_periods",
        "date_schedule",
        "is_working_day",
        "holidays",
        "PeriodType",
        "DayCountBasis",
        "DateMovingConvention",
        "EndOfMonthConvention",
        "DateScheduleFrequency",
        "DayOfWeek",
    ],
    "get_data_func": ["get_data"],
    "get_history_func": ["get_history"],
    "get_stream": ["open_pricing_stream", "PricingStream"],
    "session": ["close_session", "open_session"],
}

__getattr__, __dir__, __all__ = lazy_attach(__name__, submodules=_submodules, submod_attrs=_submod_attrs)
