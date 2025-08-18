from enum import unique
from ...._base_enum import StrEnum


@unique
class FixingFrequency(StrEnum):
    DAILY = "Daily"
    BI_WEEKLY = "BiWeekly"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"
    QUATERLY = "Quaterly"
    SEMI_ANNUAL = "SemiAnnual"
    ANNUAL = "Annual"
