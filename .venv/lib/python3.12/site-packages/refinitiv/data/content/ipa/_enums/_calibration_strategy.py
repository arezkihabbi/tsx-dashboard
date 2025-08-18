from enum import unique
from ...._base_enum import StrEnum


@unique
class CalibrationStrategy(StrEnum):
    ALL_MATURITY = "AllMaturity"
    DEFAULT = "Default"
    MGB_CALIBRATION = "MGBCalibration"
    MATURITY_BY_MATURITY = "MaturityByMaturity"
