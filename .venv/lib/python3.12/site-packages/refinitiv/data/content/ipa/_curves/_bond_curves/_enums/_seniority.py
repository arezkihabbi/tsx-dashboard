from enum import unique

from ......_base_enum import StrEnum


@unique
class Seniority(StrEnum):
    SENIOR_NON_PREFERRED = "SeniorNonPreferred"
    SENIOR_PREFERRED = "SeniorPreferred"
    SUBORDINATE_UNSECURED = "SubordinateUnsecured"
