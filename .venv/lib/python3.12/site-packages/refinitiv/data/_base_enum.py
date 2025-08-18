from enum import Enum

try:
    # Used for python 3.11 and above
    from enum import StrEnum  # pylint: disable=unused-import
except ImportError:

    class StrEnum(str, Enum):
        def __str__(self) -> str:
            return str(self.value)
