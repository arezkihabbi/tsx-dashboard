from enum import unique
from refinitiv.data._base_enum import StrEnum


@unique
class MoneynessType(StrEnum):
    FWD = "Fwd"
    SIGMA = "Sigma"
    SPOT = "Spot"
