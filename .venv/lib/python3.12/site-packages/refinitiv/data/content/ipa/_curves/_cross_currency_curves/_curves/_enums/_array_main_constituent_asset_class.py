from enum import unique

from refinitiv.data._base_enum import StrEnum


@unique
class ArrayMainConstituentAssetClass(StrEnum):
    DEPOSIT = "Deposit"
    FUTURES = "Futures"
    SWAP = "Swap"
