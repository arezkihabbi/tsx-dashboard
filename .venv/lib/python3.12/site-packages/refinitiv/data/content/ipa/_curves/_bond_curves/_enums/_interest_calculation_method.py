from enum import unique

from ......_base_enum import StrEnum


@unique
class InterestCalculationMethod(StrEnum):
    DCB_30_E_360_ISMA = "Dcb_30E_360_ISMA"
    DCB_30_360 = "Dcb_30_360"
    DCB_30_360_GERMAN = "Dcb_30_360_German"
    DCB_30_360_ISDA = "Dcb_30_360_ISDA"
    DCB_30_360_US = "Dcb_30_360_US"
    DCB_30_365_BRAZIL = "Dcb_30_365_Brazil"
    DCB_30_365_GERMAN = "Dcb_30_365_German"
    DCB_30_365_ISDA = "Dcb_30_365_ISDA"
    DCB_30_ACTUAL = "Dcb_30_Actual"
    DCB_30_ACTUAL_GERMAN = "Dcb_30_Actual_German"
    DCB_30_ACTUAL_ISDA = "Dcb_30_Actual_ISDA"
    DCB_ACTUAL_LEAP_DAY_360 = "Dcb_ActualLeapDay_360"
    DCB_ACTUAL_LEAP_DAY_365 = "Dcb_ActualLeapDay_365"
    DCB_ACTUAL_360 = "Dcb_Actual_360"
    DCB_ACTUAL_364 = "Dcb_Actual_364"
    DCB_ACTUAL_365 = "Dcb_Actual_365"
    DCB_ACTUAL_36525 = "Dcb_Actual_36525"
    DCB_ACTUAL_365_L = "Dcb_Actual_365L"
    DCB_ACTUAL_365_P = "Dcb_Actual_365P"
    DCB_ACTUAL_365_CANADIAN_CONVENTION = "Dcb_Actual_365_CanadianConvention"
    DCB_ACTUAL_ACTUAL = "Dcb_Actual_Actual"
    DCB_ACTUAL_ACTUAL_AFB = "Dcb_Actual_Actual_AFB"
    DCB_ACTUAL_ACTUAL_ISDA = "Dcb_Actual_Actual_ISDA"
    DCB_CONSTANT = "Dcb_Constant"
    DCB_WORKING_DAYS_252 = "Dcb_WorkingDays_252"
