from ..._base_enum import StrEnum


class CustomInstrumentTypes(StrEnum):
    Formula = "formula"
    UDC = "udc"
    Basket = "basket"


class SpreadAdjustmentMethod(StrEnum):
    CLOSE_TO_CLOSE = "close-to-close"
    OPEN_TO_OPEN = "open-to-open"
    CLOSE_TO_OPEN = "close-to-open"
    CLOSE_TO_OPEN_OLD_GAP = "close-to-open-old-gap"
    CLOSE_TO_OPEN_NEW_GAP = "close-to-open-new-gap"


class VolumeBasedRolloverMethod(StrEnum):
    VOLUME = "volume"
    OPEN_INTEREST = "openInterest"
    VOLUME_AND_OPEN_INTEREST = "volumeAndOpenInterest"
    VOLUME_OR_OPEN_INTEREST = "volumeOrOpenInterest"


class DayBasedRolloverMethod(StrEnum):
    DAYS_BEFORE_EXPIRY = "daysBeforeExpiry"
    DAYS_BEFORE_END_OF_MONTH = "daysBeforeEndOfMonth"
    DAYS_AFTER_BEGINNING_OF_MONTH = "daysAfterBeginningOfMonth"
