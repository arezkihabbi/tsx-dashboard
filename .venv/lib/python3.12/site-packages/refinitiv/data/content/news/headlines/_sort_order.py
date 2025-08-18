from enum import unique
from ...._base_enum import StrEnum


@unique
class SortOrder(StrEnum):
    old_to_new = "oldToNew"
    new_to_old = "newToOld"
