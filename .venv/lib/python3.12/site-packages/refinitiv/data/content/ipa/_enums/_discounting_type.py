from enum import unique

from ...._base_enum import StrEnum


@unique
class DiscountingType(StrEnum):
    LIBOR_DISCOUNTING = "LiborDiscounting"
    OIS_DISCOUNTING = "OisDiscounting"
