from enum import unique
from ...._base_enum import StrEnum


@unique
class OptionVolatilityType(StrEnum):
    HISTORICAL = "Historical"
    IMPLIED = "Implied"
    SVI_SURFACE = "SVISurface"
