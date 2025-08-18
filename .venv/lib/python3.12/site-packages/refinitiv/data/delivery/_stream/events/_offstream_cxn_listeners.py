from typing import TYPE_CHECKING

from ._cxn_listeners import CxnListeners, CxnReconnectedListener
from ._omm_cxn_listeners import ContribAckOMMListener, ContribErrorOMMListener

if TYPE_CHECKING:
    from .._offstream import _OffStreamContrib


class OffStreamCxnReconnectedListener(CxnReconnectedListener):
    def callback(self, *args, **kwargs):
        self.context.close()
        self.context.events.dispatch_reconnected(*args, **kwargs)


class OffStreamContribCxnListeners(CxnListeners):
    """
    Listeners for events from OMMStreamConnection for OffStreamContrib class
    """

    ack_listener_class = ContribAckOMMListener
    error_listener_class = ContribErrorOMMListener
    reconnected_listener_class = OffStreamCxnReconnectedListener

    def __init__(self, stream: "_OffStreamContrib") -> None:
        CxnListeners.__init__(self, stream)
        self.ack = self.ack_listener_class(stream)
        self.error = self.error_listener_class(stream)
