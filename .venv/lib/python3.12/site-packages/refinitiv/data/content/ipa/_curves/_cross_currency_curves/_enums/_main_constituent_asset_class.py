from enum import unique
from ......_base_enum import StrEnum


@unique
class MainConstituentAssetClass(StrEnum):
    FX_FORWARD = "FxForward"
    SWAP = "Swap"
