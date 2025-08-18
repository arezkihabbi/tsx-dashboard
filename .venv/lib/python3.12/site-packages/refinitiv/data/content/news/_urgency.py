from enum import unique, IntEnum


@unique
class Urgency(IntEnum):
    Hot = 1
    Exceptional = 2
    Regular = 3
    Unknown = 4
