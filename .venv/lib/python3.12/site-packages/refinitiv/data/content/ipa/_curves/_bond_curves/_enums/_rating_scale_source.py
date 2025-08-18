from enum import unique

from ......_base_enum import StrEnum


@unique
class RatingScaleSource(StrEnum):
    DBRS = "DBRS"
    FITCH = "Fitch"
    MOODYS = "Moodys"
    REFINITIV = "Refinitiv"
    S_AND_P = "SAndP"
