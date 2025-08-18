from enum import unique

from ...._base_enum import StrEnum


@unique
class FxCrossType(StrEnum):
    FX_FORWARD = "FxForward"
    FX_NON_DELIVERABLE_FORWARD = "FxNonDeliverableForward"
    FX_SPOT = "FxSpot"
    FX_SWAP = "FxSwap"
    FX_TIME_OPTION_FORWARD = "FxTimeOptionForward"
