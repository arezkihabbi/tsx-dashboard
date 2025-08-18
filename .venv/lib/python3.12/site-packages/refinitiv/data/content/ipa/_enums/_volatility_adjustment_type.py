from enum import unique
from ...._base_enum import StrEnum


@unique
class VolatilityAdjustmentType(StrEnum):
    CONSTANT_CAP = "ConstantCap"
    CONSTANT_CAPLET = "ConstantCaplet"
    NORMALIZED_CAP = "NormalizedCap"
    NORMALIZED_CAPLET = "NormalizedCaplet"
    PB_UNDEFINED = "PbUndefined"
    SHIFTED_CAP = "ShiftedCap"
