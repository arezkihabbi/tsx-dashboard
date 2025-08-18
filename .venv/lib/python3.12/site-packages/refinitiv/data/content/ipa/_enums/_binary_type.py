from enum import unique
from ...._base_enum import StrEnum


@unique
class BinaryType(StrEnum):
    DIGITAL = "Digital"
    NO_TOUCH = "NoTouch"
    NONE = "None"
    ONE_TOUCH = "OneTouch"
