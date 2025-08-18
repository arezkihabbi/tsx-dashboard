from enum import unique
from ...._base_enum import StrEnum


@unique
class CdsConvention(StrEnum):
    """
    - 'ISDA' (start_date will default to accrued_begin_date, end_date will be
      adjusted to IMM Date),
    - 'UserDefined' (start_date will default to step_in_date, end_date will not be
      adjusted).
    """

    ISDA = "ISDA"
    USER_DEFINED = "UserDefined"
