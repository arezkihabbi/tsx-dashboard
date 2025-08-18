from enum import unique

from ....._base_enum import StrEnum


@unique
class InstrumentType(StrEnum):
    BOND = "Bond"
    BOND_FUTURES = "BondFutures"
    CALENDAR_SPREAD = "CalendarSpread"
    CREDIT_DEFAULT_SWAP = "CreditDefaultSwap"
    CROSS_CURRENCY_SWAP = "CrossCurrencySwap"
    DEPOSIT = "Deposit"
    FRA = "Fra"
    FUTURES = "Futures"
    FX_FORWARD = "FxForward"
    FX_SPOT = "FxSpot"
    INTER_PRODUCT_SPREAD = "InterProductSpread"
    INTEREST_RATE_SWAP = "InterestRateSwap"
    OVERNIGHT_INDEX_SWAP = "OvernightIndexSwap"
    TENOR_BASIS_SWAP = "TenorBasisSwap"
