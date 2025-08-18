from enum import unique
from ......_base_enum import StrEnum


@unique
class CalibrationModel(StrEnum):
    BASIS_SPLINE = "BasisSpline"
    BOOTSTRAP = "Bootstrap"
    NELSON_SIEGEL_SVENSSON = "NelsonSiegelSvensson"
