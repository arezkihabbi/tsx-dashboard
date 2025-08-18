from enum import unique

from ...._base_enum import StrEnum


@unique
class SwaptionVolatilityType(StrEnum):
    ATM_SURFACE = "AtmSurface"
    SABR_VOLATILITY_CUBE = "SabrVolatilityCube"
