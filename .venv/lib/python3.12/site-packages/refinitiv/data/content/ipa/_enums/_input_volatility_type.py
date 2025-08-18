from enum import unique

from ...._base_enum import StrEnum


@unique
class InputVolatilityType(StrEnum):
    DEFAULT = "Default"
    LOG_NORMAL_VOLATILITY = "LogNormalVolatility"
    NORMALIZED_VOLATILITY = "NormalizedVolatility"
