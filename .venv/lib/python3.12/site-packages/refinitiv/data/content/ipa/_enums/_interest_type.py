from enum import unique
from ...._base_enum import StrEnum


@unique
class InterestType(StrEnum):
    """
    - 'Fixed' (the leg has a fixed coupon),
    - 'Float' (the leg has a floating rate index). Mandatory.
    """

    FIXED = "Fixed"
    FLOAT = "Float"
    STEPPED = "Stepped"
