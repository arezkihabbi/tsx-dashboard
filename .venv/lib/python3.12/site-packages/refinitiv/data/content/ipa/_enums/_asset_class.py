from enum import unique
from ...._base_enum import StrEnum


@unique
class AssetClass(StrEnum):
    FUTURES = "Futures"
    SWAP = "Swap"
