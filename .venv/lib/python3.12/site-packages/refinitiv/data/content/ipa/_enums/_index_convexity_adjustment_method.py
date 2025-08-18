from enum import unique

from ...._base_enum import StrEnum


@unique
class IndexConvexityAdjustmentMethod(StrEnum):
    BLACK_SCHOLES = "BlackScholes"
    LINEAR_SWAP_MODEL = "LinearSwapModel"
    NONE = "None"
    REPLICATION = "Replication"
