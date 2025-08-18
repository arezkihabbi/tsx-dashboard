from enum import unique

from ...._base_enum import StrEnum


@unique
class IndexResetType(StrEnum):
    """
    - InAdvance (resets the index before the start of the interest period),
    - InArrears (resets the index at the end of the interest period)
    """

    IN_ADVANCE = "InAdvance"
    IN_ARREARS = "InArrears"
