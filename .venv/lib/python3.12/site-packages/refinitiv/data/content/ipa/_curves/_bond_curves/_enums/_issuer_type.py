from enum import unique

from ......_base_enum import StrEnum


@unique
class IssuerType(StrEnum):
    AGENCY = "Agency"
    CORPORATE = "Corporate"
    MUNIS = "Munis"
    NON_FINANCIALS = "NonFinancials"
    SOVEREIGN = "Sovereign"
    SUPRANATIONAL = "Supranational"
