from enum import unique
from ...._base_enum import StrEnum


@unique
class BenchmarkYieldSelectionMode(StrEnum):
    INTERPOLATE = "Interpolate"
    NEAREST = "Nearest"
