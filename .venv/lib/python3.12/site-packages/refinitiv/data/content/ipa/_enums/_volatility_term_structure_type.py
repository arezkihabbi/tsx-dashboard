from enum import unique

from ...._base_enum import StrEnum


@unique
class VolatilityTermStructureType(StrEnum):
    HISTORICAL = "Historical"
    IMPLIED = "Implied"
