from enum import unique
from ...._base_enum import StrEnum


@unique
class AmericanMonteCarloMethod(StrEnum):
    ANDERSEN = "Andersen"
    LONGSTAFF_SCHWARTZ = "LongstaffSchwartz"
