from enum import unique

from ....._base_enum import StrEnum


@unique
class SwapPriceSide(StrEnum):
    ASK = "Ask"
    BID = "Bid"
    MID = "Mid"
