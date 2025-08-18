from enum import unique
from ...._base_enum import StrEnum


@unique
class SwaptionType(StrEnum):
    PAYER = "Payer"
    RECEIVER = "Receiver"
