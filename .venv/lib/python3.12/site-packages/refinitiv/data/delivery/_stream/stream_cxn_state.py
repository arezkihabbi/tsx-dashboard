from enum import Enum, unique, auto


@unique
class StreamCxnState(Enum):
    Initial = auto()
    Connecting = auto()
    MessageProcessing = auto()
    Disconnecting = auto()
    Disconnected = auto()
    Disposed = auto()
