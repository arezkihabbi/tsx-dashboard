from enum import unique

from ...._base_enum import StrEnum


@unique
class PremiumSettlementType(StrEnum):
    FORWARD = "Forward"
    SCHEDULE = "Schedule"
    SPOT = "Spot"
