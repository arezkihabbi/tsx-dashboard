from enum import unique

from ...._base_enum import StrEnum


@unique
class StubRule(StrEnum):
    """
    - ShortFirstProRata (to create a short period between the start date and the
      first coupon date, and pay a smaller amount of interest for the short
      period.All coupon dates are calculated backward from the maturity date),
    - ShortFirstFull (to create a short period between the start date and the first
      coupon date, and pay a regular coupon on the first coupon date. All coupon
      dates are calculated backward from the maturity date),
    - LongFirstFull (to create a long period between the start date and the second
      coupon date, and pay a regular coupon on the second coupon date. All coupon
      dates are calculated backward from the maturity date),
    - ShortLastProRata (to create a short period between the last payment date and
      maturity, and pay a smaller amount of interest for the short period. All
      coupon dates are calculated forward from the start date). This property may
      also be used in conjunction with first_regular_payment_date and
      last_regular_payment_date; in that case the following values can be defined:
    - Issue (all dates are aligned on the issue date),
    - Maturity (all dates are aligned on the maturity date).
    """

    ISSUE = "Issue"
    LONG_FIRST_FULL = "LongFirstFull"
    MATURITY = "Maturity"
    SHORT_FIRST_FULL = "ShortFirstFull"
    SHORT_FIRST_PRO_RATA = "ShortFirstProRata"
    SHORT_LAST_PRO_RATA = "ShortLastProRata"
