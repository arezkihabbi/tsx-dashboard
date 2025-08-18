from enum import unique
from ......_base_enum import StrEnum


@unique
class BasisSplineSmoothModel(StrEnum):
    ANDERSON_SMOOTHING_SPLINE_MODEL = "AndersonSmoothingSplineModel"
    MC_CULLOCH_LINEAR_REGRESSION = "McCullochLinearRegression"
    WAGGONER_SMOOTHING_SPLINE_MODEL = "WaggonerSmoothingSplineModel"
