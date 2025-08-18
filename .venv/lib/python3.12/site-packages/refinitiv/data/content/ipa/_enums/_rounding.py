from enum import unique
from ...._base_enum import StrEnum


@unique
class Rounding(StrEnum):
    DEFAULT = "Default"
    EIGHT = "Eight"
    FIVE = "Five"
    FOUR = "Four"
    ONE = "One"
    SEVEN = "Seven"
    SIX = "Six"
    THREE = "Three"
    TWO = "Two"
    UNROUNDED = "Unrounded"
    ZERO = "Zero"
