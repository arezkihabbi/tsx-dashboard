from typing import TYPE_CHECKING

from .event_code import EventCode
from ..._listener import EventListener

if TYPE_CHECKING:
    from . import Session
    from ..stream_connection import StreamConnection  # noqa: F401


class CxnListener(EventListener["Session"]):
    event_code: EventCode = None

    def callback(self, originator: "StreamConnection", *args, **kwargs):
        try:
            message: dict = args[0]
        except IndexError:
            message = {}

        message["url"] = originator._config.url
        message["api_cfg"] = originator._config.api_cfg_key
        self.context._call_on_event(self.event_code, message)


class CxnConnectingListener(CxnListener):
    event_code = EventCode.StreamConnecting


class CxnConnectedListener(CxnListener):
    event_code = EventCode.StreamConnected


class CxnDisconnectedListener(CxnListener):
    event_code = EventCode.StreamDisconnected


class CxnReconnectingListener(CxnListener):
    event_code = EventCode.StreamReconnecting


class CxnLoginSuccessListener(CxnListener):
    event_code = EventCode.StreamAuthenticationSuccess


class CxnLoginFailListener(CxnListener):
    event_code = EventCode.StreamAuthenticationFailed


class CxnListeners:
    """
    Event listeners for StreamConnection.
    """

    def __init__(self, context: "Session") -> None:
        super().__init__()
        self.connecting = CxnConnectingListener(context)
        self.connected = CxnConnectedListener(context)
        self.disconnected = CxnDisconnectedListener(context)
        self.reconnecting = CxnReconnectingListener(context)
        self.login_success = CxnLoginSuccessListener(context)
        self.login_fail = CxnLoginFailListener(context)
