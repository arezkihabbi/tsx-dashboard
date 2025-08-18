from enum import unique

from ...._base_enum import StrEnum


@unique
class TenorReferenceDate(StrEnum):
    SPOT_DATE = "SpotDate"
    VALUATION_DATE = "ValuationDate"
