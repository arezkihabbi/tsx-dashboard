from enum import Enum, auto


class SessionCxnType(Enum):
    DEPLOYED = auto()
    REFINITIV_DATA = auto()
    REFINITIV_DATA_AND_DEPLOYED = auto()
    DESKTOP = auto()
    NONE = auto()
