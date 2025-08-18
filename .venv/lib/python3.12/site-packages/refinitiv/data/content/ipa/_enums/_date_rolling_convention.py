from enum import unique

from ...._base_enum import StrEnum


@unique
class DateRollingConvention(StrEnum):
    """
    - Last (For setting the calculated date to the last working day),
    - Last28 (For setting the calculated date to the last working day. 28FEB being
      always considered as the last working day),
    - Same (For setting the calculated date to the same day . In this latter case,
      the date may be moved according to the date moving convention if it is a
      non-working day),
    - Same28 (For setting the calculated date to the same day .28FEB being always
      considered as the last working day).
    """

    LAST = "Last"
    LAST28 = "Last28"
    SAME = "Same"
    SAME28 = "Same28"
