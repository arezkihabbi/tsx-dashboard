from enum import unique
from refinitiv.data._base_enum import StrEnum


@unique
class SurfaceOutputs(StrEnum):
    HEADERS = "Headers"
    DATATYPE = "DataType"
    DATA = "Data"
    STATUSES = "Statuses"
    FORWARD_CURVE = "ForwardCurve"
    DIVIDENDS = "Dividends"
    INTEREST_RATE_CURVE = "InterestRateCurve"
    GOODNESS_OF_FIT = "GoodnessOfFit"
    UNDERLYING_SPOT = "UnderlyingSpot"
    DISCOUNT_CURVE = "DiscountCurve"
    MONEYNESS_STRIKE = "MoneynessStrike"
