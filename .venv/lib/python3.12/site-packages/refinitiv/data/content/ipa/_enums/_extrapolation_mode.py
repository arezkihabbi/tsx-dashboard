from enum import unique

from ...._base_enum import StrEnum


@unique
class ExtrapolationMode(StrEnum):
    CONSTANT = "Constant"
    LINEAR = "Linear"
    NONE = "None"
