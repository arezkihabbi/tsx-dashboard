from enum import unique

from ...._base_enum import StrEnum


@unique
class VolatilityModel(StrEnum):
    CUBIC_SPLINE = "CubicSpline"
    SABR = "SABR"
    SVI = "SVI"
    TWIN_LOGNORMAL = "TwinLognormal"
