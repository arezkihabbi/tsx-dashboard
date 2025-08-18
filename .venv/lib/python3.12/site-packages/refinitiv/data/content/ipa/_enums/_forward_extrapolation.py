from enum import unique

from ...._base_enum import StrEnum


@unique
class ForwardExtrapolation(StrEnum):
    CST_EXTRAPOL = "Cst_Extrapol"
    LINEAR_EXTRAPOL = "Linear_Extrapol"
    POWER_GROWTH_EXTRAPOL = "PowerGrowth_Extrapol"
    USE_DIVIDEND_EXTRAPOL = "UseDividendExtrapol"
