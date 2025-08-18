__all__ = (
    "get_data",
    "get_news_headlines",
    "get_news_story",
    "get_symbology",
    "get_timeseries",
    "set_app_key",
    "set_log_level",
    "StreamingPrices",
    "TR_Field",
)

import warnings as _warnings

_warnings.warn(
    "The refinitiv.data.eikon module will be removed in future library version v2.0. "
    "Please install and use the 'eikon' Python library instead or migrate your code to the Refinitiv/LSEG Data Library",
    category=FutureWarning,
)

from ._data_grid import TR_Field, get_data
from ._news_request import get_news_headlines, get_news_story
from ._symbology import get_symbology
from ._time_series import get_timeseries
from ._tools import set_app_key, set_log_level
from ._streaming_prices import StreamingPrices
