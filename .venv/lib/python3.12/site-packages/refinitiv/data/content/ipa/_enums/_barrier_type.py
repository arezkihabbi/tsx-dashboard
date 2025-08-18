from enum import unique
from ...._base_enum import StrEnum


@unique
class BarrierType(StrEnum):
    KNOCK_IN = "KnockIn"
    KNOCK_IN_KNOCK_OUT = "KnockInKnockOut"
    KNOCK_OUT = "KnockOut"
    KNOCK_OUT_KNOCK_IN = "KnockOutKnockIn"
