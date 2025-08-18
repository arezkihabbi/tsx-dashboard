from enum import Enum, auto


class ProtocolType(Enum):
    NONE = auto()
    OMM = auto()
    OMM_OFF_CONTRIB = auto()
    RDP = auto()
