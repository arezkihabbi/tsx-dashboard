from enum import unique
from ...._base_enum import StrEnum


@unique
class BusinessDayConvention(StrEnum):
    """
    - BbswModifiedFollowing (adjusts dates  according to the BBSW Modified Following
      convention),
    - ModifiedFollowing (adjusts dates according to the Modified Following
      convention - next business day unless is it goes into the next month,
      preceeding is used in that  case),
    - NextBusinessDay (adjusts dates according to the Following convention - Next
      Business Day),
    - NoMoving (does not adjust dates),
    - PreviousBusinessDay (adjusts dates  according to the Preceeding convention -
      Previous Business Day).
    """

    BBSW_MODIFIED_FOLLOWING = "BbswModifiedFollowing"
    EVERY_THIRD_WEDNESDAY = "EveryThirdWednesday"
    MODIFIED_FOLLOWING = "ModifiedFollowing"
    NEXT_BUSINESS_DAY = "NextBusinessDay"
    NO_MOVING = "NoMoving"
    PREVIOUS_BUSINESS_DAY = "PreviousBusinessDay"
