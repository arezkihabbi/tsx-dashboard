from enum import unique

from ...._base_enum import StrEnum


@unique
class YieldType(StrEnum):
    ANNUAL_EQUIVALENT = "Annual_Equivalent"
    BOND_ACTUAL_364 = "Bond_Actual_364"
    BRAESS_FANGMEYER = "Braess_Fangmeyer"
    DISCOUNT_ACTUAL_360 = "Discount_Actual_360"
    DISCOUNT_ACTUAL_365 = "Discount_Actual_365"
    EUROLAND = "Euroland"
    ISMA = "Isma"
    JAPANESE_COMPOUNDED = "Japanese_Compounded"
    JAPANESE_SIMPLE = "Japanese_Simple"
    MONEY_MARKET_ACTUAL_360 = "MoneyMarket_Actual_360"
    MONEY_MARKET_ACTUAL_365 = "MoneyMarket_Actual_365"
    MONEY_MARKET_ACTUAL_ACTUAL = "MoneyMarket_Actual_Actual"
    MOOSMUELLER = "Moosmueller"
    NATIVE = "Native"
    QUARTERLY_EQUIVALENT = "Quarterly_Equivalent"
    SEMIANNUAL_EQUIVALENT = "Semiannual_Equivalent"
    TURKISH_COMPOUNDED = "TurkishCompounded"
    US_GOVT = "UsGovt"
    US_T_BILLS = "UsTBills"
    WEEKEND = "Weekend"
