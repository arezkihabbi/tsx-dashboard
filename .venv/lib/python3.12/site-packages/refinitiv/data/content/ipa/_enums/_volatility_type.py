from enum import unique

from ...._base_enum import StrEnum


@unique
class VolatilityType(StrEnum):
    FLAT = "Flat"
    TERM_STRUCTURE = "TermStructure"
