from enum import unique

from ......._base_enum import StrEnum


@unique
class QuotationMode(StrEnum):
    OUTRIGHT = "Outright"
    SWAP_POINT = "SwapPoint"
