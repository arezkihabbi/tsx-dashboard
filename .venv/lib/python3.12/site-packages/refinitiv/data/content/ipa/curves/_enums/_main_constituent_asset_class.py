from enum import unique
from ....._base_enum import StrEnum


@unique
class MainConstituentAssetClass(StrEnum):
    FUTURES = "Futures"
    SWAP = "Swap"
