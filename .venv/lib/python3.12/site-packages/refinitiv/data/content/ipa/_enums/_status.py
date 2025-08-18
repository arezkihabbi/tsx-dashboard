from enum import unique

from ...._base_enum import StrEnum


@unique
class Status(StrEnum):
    NOT_APPLICABLE = "NotApplicable"
    USER = "User"
    DATA = "Data"
    COMPUTED = "Computed"
    ERROR = "Error"
    NONE = "None"
