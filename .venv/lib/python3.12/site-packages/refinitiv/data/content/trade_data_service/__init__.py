__all__ = (
    "Definition",
    "Events",
    "FinalizedOrders",
    "UniverseTypes",
)

import warnings as _warnings

from ._definition import Definition
from ._stream import Events
from ._stream import FinalizedOrders
from ._stream import UniverseTypes

_warnings.warn(
    "The Trade Data Service has been discontinued. "
    "The rd.content.trade_data_service module will be removed in future library version v2.0.",
    category=FutureWarning,
)
