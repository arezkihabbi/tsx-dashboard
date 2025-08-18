from enum import unique

from ......_base_enum import StrEnum


@unique
class MainConstituentAssetClass(StrEnum):
    BOND = "Bond"
    CREDIT_DEFAULT_SWAP = "CreditDefaultSwap"
