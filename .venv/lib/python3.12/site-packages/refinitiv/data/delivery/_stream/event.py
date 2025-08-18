from enum import Enum, unique, auto
from typing import Any


@unique
class StreamEvtID(Enum):
    UPDATE = 0.1
    REFRESH = 0.2
    STATUS = 0.3
    COMPLETE = 0.4
    ERROR = 0.5
    ACK = 0.6
    RESPONSE = 0.7
    ALARM = 0.8
    HEARTBEAT = 0.9

    def __add__(self, other: int) -> float:
        return other + self.value

    def __radd__(self, other: int) -> float:
        return self.__add__(other)

    def __contains__(self, item: float) -> bool:
        return str(item)[-1] == str(self.value)[-1]


@unique
class StreamStEvt(Enum):
    OPEN = auto()
    CLOSE = auto()

    def __contains__(self, item: Any) -> bool:
        return False


@unique
class StreamEvt(Enum):
    UPDATE = auto()
    REFRESH = auto()
    STATUS = auto()
    COMPLETE = auto()
    ERROR = auto()
    ACK = auto()
    RESPONSE = auto()
    ALARM = auto()

    def __contains__(self, item: Any) -> bool:
        return False


@unique
class CxnEvent(Enum):
    CONNECTING = auto()
    CONNECTED = auto()
    READY = auto()
    DISCONNECTING = auto()
    DISCONNECTED = auto()
    DISPOSED = auto()
    RECONNECTING = auto()
    RECONNECTED = auto()
    LOGIN_SUCCESS = auto()
    LOGIN_FAIL = auto()

    def __contains__(self, item: Any) -> bool:
        return False
