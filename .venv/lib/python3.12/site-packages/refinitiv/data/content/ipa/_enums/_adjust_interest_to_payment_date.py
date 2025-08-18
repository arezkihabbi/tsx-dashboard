from enum import unique
from ...._base_enum import StrEnum


@unique
class AdjustInterestToPaymentDate(StrEnum):
    ADJUSTED = "Adjusted"
    UNADJUSTED = "Unadjusted"
