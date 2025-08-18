from enum import unique
from ....._base_enum import StrEnum


@unique
class MarketDataAccessDeniedFallback(StrEnum):
    IGNORE_CONSTITUENTS = "IgnoreConstituents"
    RETURN_ERROR = "ReturnError"
    USE_DELAYED_DATA = "UseDelayedData"
