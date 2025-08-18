from enum import unique

from ...._base_enum import StrEnum


@unique
class ImpliedDepositDateConvention(StrEnum):
    FX_MARKET_CONVENTION = "FxMarketConvention"
    MONEY_MARKET_CONVENTION = "MoneyMarketConvention"
