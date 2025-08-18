from enum import unique

from ...._base_enum import StrEnum


@unique
class RoundingType(StrEnum):
    CEIL = "Ceil"
    DEFAULT = "Default"
    DOWN = "Down"
    FACE_DOWN = "FaceDown"
    FACE_NEAR = "FaceNear"
    FACE_UP = "FaceUp"
    FLOOR = "Floor"
    NEAR = "Near"
    UP = "Up"
