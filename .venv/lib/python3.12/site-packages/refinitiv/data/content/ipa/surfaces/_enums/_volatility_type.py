from enum import Enum, unique


@unique
class VolatilityType(Enum):
    LOG_NORMAL_VOLATILITY = "LogNormalVolatility"
    NORMAL_VOLATILITY = "NormalVolatility"
