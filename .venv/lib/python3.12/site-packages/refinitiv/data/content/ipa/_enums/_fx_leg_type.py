from enum import unique
from ...._base_enum import StrEnum


@unique
class FxLegType(StrEnum):
    FX_FORWARD = "FxForward"
    FX_NON_DELIVERABLE_FORWARD = "FxNonDeliverableForward"
    FX_SPOT = "FxSpot"
    SWAP_FAR = "SwapFar"
    SWAP_NEAR = "SwapNear"
