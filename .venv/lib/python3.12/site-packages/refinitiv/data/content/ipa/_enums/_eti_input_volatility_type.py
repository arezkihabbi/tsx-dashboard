from enum import unique

from ...._base_enum import StrEnum


@unique
class EtiInputVolatilityType(StrEnum):
    IMPLIED = "Implied"
    QUOTED = "Quoted"
    SETTLE = "Settle"
