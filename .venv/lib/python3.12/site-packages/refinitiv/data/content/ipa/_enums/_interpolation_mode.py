from enum import unique
from ...._base_enum import StrEnum


@unique
class InterpolationMode(StrEnum):
    CUBIC_DISCOUNT = "CubicDiscount"
    CUBIC_RATE = "CubicRate"
    CUBIC_SPLINE = "CubicSpline"
    FORWARD_MONOTONE_CONVEX = "ForwardMonotoneConvex"
    LINEAR = "Linear"
    LOG = "Log"
