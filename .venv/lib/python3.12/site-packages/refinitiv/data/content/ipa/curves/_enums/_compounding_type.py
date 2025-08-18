from enum import unique

from ....._base_enum import StrEnum


@unique
class CompoundingType(StrEnum):
    COMPOUNDED = "Compounded"
    CONTINUOUS = "Continuous"
    DISCOUNTED = "Discounted"
    MONEY_MARKET = "MoneyMarket"
