from enum import unique
from ...._base_enum import StrEnum


@unique
class SwaptionSettlementType(StrEnum):
    CCP = "CCP"
    CASH = "Cash"
    PHYSICAL = "Physical"
