from enum import unique
from ...._base_enum import StrEnum


@unique
class FxBinaryType(StrEnum):
    """
    - onetouchimmediate: the option expires in-the-money if the trigger is reached
      at any time prior to option expiration.the option premium is paid immediately.
    - onetouchdeferred: the option expires in-the-money if the trigger is reached at
      any time prior to option expiration. the option premium payment is deferred.
    - notouch: the option expires in-the-money if the trigger is not reached prior
      to expiration.
    - digital: the option expires in-the-money if the trigger is reached at the
      option expiry date. mandatory for binary options.
    """

    DIGITAL = "Digital"
    NO_TOUCH = "NoTouch"
    NONE = "None"
    ONE_TOUCH_DEFERRED = "OneTouchDeferred"
    ONE_TOUCH_IMMEDIATE = "OneTouchImmediate"
