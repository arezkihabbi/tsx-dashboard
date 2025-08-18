from enum import unique

from ...._base_enum import StrEnum


@unique
class IndexCompoundingMethod(StrEnum):
    """
    - Compounded (uses the compounded average rate from multiple fixings),
    - Average (uses the arithmetic average rate from multiple fixings),
    - Constant (uses the last published rate among multiple fixings),
    - AdjustedCompounded (uses Chinese 7-day repo fixing),
    - MexicanCompounded (uses Mexican Bremse fixing).
    """

    COMPOUNDED = "Compounded"
    AVERAGE = "Average"
    CONSTANT = "Constant"
    ADJUSTED_COMPOUNDED = "AdjustedCompounded"
    MEXICAN_COMPOUNDED = "MexicanCompounded"
