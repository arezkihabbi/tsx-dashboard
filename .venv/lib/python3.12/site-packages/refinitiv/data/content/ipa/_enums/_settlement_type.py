from enum import unique
from ...._base_enum import StrEnum


@unique
class SettlementType(StrEnum):
    """
    - physical(asset): delivering the underlying asset.
    - cash: paying out in cash.
    """

    ASSET = "Asset"
    CASH = "Cash"
    PHYSICAL = "Physical"
    UNDEFINED = "Undefined"
