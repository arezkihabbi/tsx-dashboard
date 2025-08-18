from enum import unique

from ...._base_enum import StrEnum


@unique
class DateMovingConvention(StrEnum):
    """
    The method to adjust dates.

    The possible values are:
        - BbswModifiedFollowing - Adjusts dates according to the BBSW Modified Following convention.
        - EveryThirdWednesday - dates are adjusted to the next every third Wednesday.
        - ModifiedFollowing - Adjusts dates according to the Modified Following
            convention - next business day unless it goes
            to the next month, preceding is used in that case.
        - NextBusinessDay - move to following date when public holiday.
        - NoMoving - no moving convention.
        - PreviousBusinessDay - move to preceding date when public holiday.
    """

    BBSW_MODIFIED_FOLLOWING = "BbswModifiedFollowing"
    EVERY_THIRD_WEDNESDAY = "EveryThirdWednesday"
    MODIFIED_FOLLOWING = "ModifiedFollowing"
    NEXT_BUSINESS_DAY = "NextBusinessDay"
    NO_MOVING = "NoMoving"
    PREVIOUS_BUSINESS_DAY = "PreviousBusinessDay"
