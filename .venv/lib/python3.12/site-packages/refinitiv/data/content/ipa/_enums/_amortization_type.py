from enum import unique
from ...._base_enum import StrEnum


@unique
class AmortizationType(StrEnum):
    ANNUITY = "Annuity"
    LINEAR = "Linear"
    NONE = "None"
    SCHEDULE = "Schedule"
