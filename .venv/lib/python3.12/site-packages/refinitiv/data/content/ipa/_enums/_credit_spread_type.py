from enum import unique

from ...._base_enum import StrEnum


@unique
class CreditSpreadType(StrEnum):
    FLAT_SPREAD = "FlatSpread"
    TERM_STRUCTURE = "TermStructure"
