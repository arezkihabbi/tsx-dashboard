from enum import unique

from ...._base_enum import StrEnum


@unique
class RepoCurveType(StrEnum):
    DEPOSIT_CURVE = "DepositCurve"
    LIBOR_FIXING = "LiborFixing"
    REPO_CURVE = "RepoCurve"
