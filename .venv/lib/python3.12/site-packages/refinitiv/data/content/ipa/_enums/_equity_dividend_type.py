from enum import unique
from ...._base_enum import StrEnum


@unique
class EquityDividendType(StrEnum):
    DEFAULT = "Default"
    DISCRETE = "Discrete"
    YIELD = "Yield"
