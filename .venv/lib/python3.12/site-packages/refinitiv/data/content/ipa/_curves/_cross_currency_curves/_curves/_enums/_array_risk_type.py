from enum import unique

from refinitiv.data._base_enum import StrEnum


@unique
class ArrayRiskType(StrEnum):
    INTEREST_RATE = "InterestRate"
