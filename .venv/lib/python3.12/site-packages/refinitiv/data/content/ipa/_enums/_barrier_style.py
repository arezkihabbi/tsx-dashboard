from enum import unique
from ...._base_enum import StrEnum


@unique
class BarrierStyle(StrEnum):
    AMERICAN = "American"
    EUROPEAN = "European"
    NONE = "None"
