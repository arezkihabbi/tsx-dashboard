from enum import unique

from ...._base_enum import StrEnum


@unique
class DoubleBinaryType(StrEnum):
    """
    - DoubleNoTouch: the option expires in-the-money if the price of the underlying
      asset fails to breach either the lower trigger or the upper trigger at any
      time prior to option expiration.
    """

    DOUBLE_NO_TOUCH = "DoubleNoTouch"
    NONE = "None"
