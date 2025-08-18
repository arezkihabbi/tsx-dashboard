from enum import unique
from ..._base_enum import StrEnum


@unique
class Package(StrEnum):
    """
    BASIC - A limited set of fields with a single historical point which could typically be considered 'Free to Air' content

    STANDARD - The common fields for a content set with a limited amount of history

    PROFESSIONAL - All fields and all history for a particular content set
    """

    BASIC = "basic"
    STANDARD = "standard"
    PROFESSIONAL = "professional"
