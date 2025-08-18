from enum import unique

from ...._base_enum import StrEnum


@unique
class ExerciseScheduleType(StrEnum):
    FIXED_LEG = "FixedLeg"
    FLOAT_LEG = "FloatLeg"
    USER_DEFINED = "UserDefined"
