from enum import unique

from ...._base_enum import StrEnum


@unique
class UpOrDown(StrEnum):
    DOWN = "Down"
    UP = "Up"
