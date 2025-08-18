from enum import unique
from ...._base_enum import StrEnum


@unique
class InterestCalculationConvention(StrEnum):
    BOND_BASIS = "BondBasis"
    MONEY_MARKET = "MoneyMarket"
    NONE = "None"
