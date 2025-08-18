from enum import unique

from ......_base_enum import StrEnum


@unique
class PriceSide(StrEnum):
    ASK = "Ask"
    BID = "Bid"
    MID = "Mid"
