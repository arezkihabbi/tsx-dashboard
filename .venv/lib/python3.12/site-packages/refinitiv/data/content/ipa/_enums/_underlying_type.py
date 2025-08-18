from enum import unique

from ...._base_enum import StrEnum


@unique
class UnderlyingType(StrEnum):
    ETI = "Eti"
    FX = "Fx"
    CAP = "Cap"
    SWAPTION = "Swaption"
