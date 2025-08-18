from enum import unique
from ...._base_enum import StrEnum


@unique
class IndexConvexityAdjustmentType(StrEnum):
    NONE = "None"
    BLACK_SCHOLES = "BlackScholes"
    REPLICATION = "Replication"
    LIBOR_SWAP_METHOD = "LiborSwapMethod"
