from enum import unique
from ...._base_enum import StrEnum


@unique
class AverageType(StrEnum):
    ARITHMETIC_RATE = "ArithmeticRate"
    ARITHMETIC_STRIKE = "ArithmeticStrike"
    GEOMETRIC_RATE = "GeometricRate"
    GEOMETRIC_STRIKE = "GeometricStrike"
