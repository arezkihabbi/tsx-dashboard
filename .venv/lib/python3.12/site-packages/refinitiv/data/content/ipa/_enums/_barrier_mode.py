from enum import unique
from ...._base_enum import StrEnum


@unique
class BarrierMode(StrEnum):
    AMERICAN = "American"
    EARLY_END_WINDOW = "EarlyEndWindow"
    EUROPEAN = "European"
    FORWARD_START_WINDOW = "ForwardStartWindow"
    UNDEFINED = "Undefined"
