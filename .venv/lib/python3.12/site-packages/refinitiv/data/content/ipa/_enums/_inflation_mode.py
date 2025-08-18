from enum import unique
from ...._base_enum import StrEnum


@unique
class InflationMode(StrEnum):
    ADJUSTED = "Adjusted"
    DEFAULT = "Default"
    UNADJUSTED = "Unadjusted"
