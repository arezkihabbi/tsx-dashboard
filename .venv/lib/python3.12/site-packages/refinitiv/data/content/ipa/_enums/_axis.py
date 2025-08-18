from enum import unique
from ...._base_enum import StrEnum


@unique
class Axis(StrEnum):
    """
    The enumerate that specifies the unit for the axis.
    """

    X = "X"
    Y = "Y"
    Z = "Z"
    DATE = "Date"
    DELTA = "Delta"
    EXPIRY = "Expiry"
    MONEYNESS = "Moneyness"
    STRIKE = "Strike"
    TENOR = "Tenor"
