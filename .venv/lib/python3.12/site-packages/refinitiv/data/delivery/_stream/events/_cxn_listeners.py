from typing import TYPE_CHECKING

from ...._listener import EventListener

if TYPE_CHECKING:
    from ..stream_connection import StreamConnection  # noqa: F401
    from .._stream import Stream  # noqa: F401


class CxnReconnectedListener(EventListener["Stream"]):
    """
    Reconnected event listener for StreamConnection.
    """

    def callback(self, *args, **kwargs):
        stream = self.context
        stream.send(stream.open_message)
        stream.events.dispatch_reconnected(*args, **kwargs)


class CxnDisconnectingListener(EventListener["Stream"]):
    """
    Disconnecting event listener for StreamConnection.
    """

    def callback(self, *args, **kwargs):
        stream = self.context
        stream.close()
        stream.events.dispatch_disconnecting(*args, **kwargs)


class CxnDisposedListener(EventListener["Stream"]):
    """
    Disposed event listener for StreamConnection.
    """

    def callback(self, *args, **kwargs):
        stream = self.context
        stream.close()
        stream.events.dispatch_disposed(*args, **kwargs)


class CxnListeners:
    """
    Event listeners for StreamConnection.
    """

    disconnecting_listener_class = CxnDisconnectingListener
    reconnected_listener_class = CxnReconnectedListener
    disposed_listener_class = CxnDisposedListener

    def __init__(self, stream: "Stream") -> None:
        super().__init__()
        self.disconnecting = self.disconnecting_listener_class(stream)
        self.reconnected = self.reconnected_listener_class(stream)
        self.disposed = self.disposed_listener_class(stream)
