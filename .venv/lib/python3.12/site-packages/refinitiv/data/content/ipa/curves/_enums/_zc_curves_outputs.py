from enum import unique

from ....._base_enum import StrEnum


@unique
class ZcCurvesOutputs(StrEnum):
    CONSTITUENTS = "Constituents"
    DETAILED_CURVE_POINT = "DetailedCurvePoint"
