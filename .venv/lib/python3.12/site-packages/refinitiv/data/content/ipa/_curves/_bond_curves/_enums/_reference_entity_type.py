from enum import unique

from ......_base_enum import StrEnum


@unique
class ReferenceEntityType(StrEnum):
    BOND_ISIN = "BondIsin"
    BOND_RIC = "BondRic"
    CHAIN_RIC = "ChainRic"
    ORGANISATION_ID = "OrganisationId"
    TICKER = "Ticker"
