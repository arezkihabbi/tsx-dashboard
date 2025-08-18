from enum import unique

from ...._base_enum import StrEnum


@unique
class IndexObservationMethod(StrEnum):
    """
    - Lookback (uses the interest period for both rate accrual and interest payment),
    - PeriodShift (uses the observation period for both rate accrual and interest payment),
    - Mixed (uses the observation period for rate accrual and the interest period for interest payment).
    """

    LOOKBACK = "Lookback"
    MIXED = "Mixed"
    PERIOD_SHIFT = "PeriodShift"
