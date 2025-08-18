from enum import unique

from ......_base_enum import StrEnum


@unique
class InterpolationMode(StrEnum):
    CUBIC_SPLINE = "CubicSpline"
    LINEAR = "Linear"
    LOG = "Log"
