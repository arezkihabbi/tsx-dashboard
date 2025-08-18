from enum import unique

from ....._base_enum import StrEnum


@unique
class UnderlyingType(StrEnum):
    """
    The possible values are:
        - Eti: eti(exchanged traded instruments) options,
        - Fx: fx options.
    """

    ETI = "Eti"
    FX = "Fx"
