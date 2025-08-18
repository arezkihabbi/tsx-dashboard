from enum import unique

from ...._base_enum import StrEnum


@unique
class InOrOut(StrEnum):
    IN = "In"
    OUT = "Out"
