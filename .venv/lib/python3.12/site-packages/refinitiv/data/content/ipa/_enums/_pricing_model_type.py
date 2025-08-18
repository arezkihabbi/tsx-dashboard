from enum import unique
from ...._base_enum import StrEnum


@unique
class PricingModelType(StrEnum):
    BINOMIAL = "Binomial"
    BLACK_SCHOLES = "BlackScholes"
    LOCAL_VOLATILITY = "LocalVolatility"
    TRINOMIAL = "Trinomial"
    VANNA_VOLGA = "VannaVolga"
    WHALEY = "Whaley"
