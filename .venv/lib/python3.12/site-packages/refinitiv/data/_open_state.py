from enum import unique, Enum


@unique
class OpenState(Enum):
    """
    Session lifecycle state.
        Opened : the session is open and ready to work.
        Pending : the session is waiting to be opened or closed.
        Closed : the session is closed.
    """

    Opened = "Opened"
    Pending = "Pending"
    Closed = "Closed"
