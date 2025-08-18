from enum import unique
from ...._base_enum import StrEnum


@unique
class VolType(StrEnum):
    CALL = "Call"
    PUT = "Put"
