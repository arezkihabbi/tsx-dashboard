from functools import partialmethod
from typing import TYPE_CHECKING

from ._events import Events_CallbackHandler
from ..event import CxnEvent, StreamEvtID

if TYPE_CHECKING:
    from .. import StreamConnection  # noqa: F401


def dispatch_msg(self: Events_CallbackHandler, ev: CxnEvent, message: dict):
    self.dispatch(ev, message)


def dispatch_stream_id(self: Events_CallbackHandler, ev: StreamEvtID, stream_id: float, message: dict):
    self.dispatch(stream_id + ev, message)


class CxnEvts(Events_CallbackHandler["CxnEvts", "StreamConnection"]):
    """
    Events for StreamConnection
    """

    on_connecting = partialmethod(Events_CallbackHandler.on, CxnEvent.CONNECTING)
    on_connected = partialmethod(Events_CallbackHandler.on, CxnEvent.CONNECTED)
    on_reconnecting = partialmethod(Events_CallbackHandler.on, CxnEvent.RECONNECTING)
    on_reconnected = partialmethod(Events_CallbackHandler.on, CxnEvent.RECONNECTED)
    on_disconnecting = partialmethod(Events_CallbackHandler.on, CxnEvent.DISCONNECTING)
    on_disconnected = partialmethod(Events_CallbackHandler.on, CxnEvent.DISCONNECTED)
    on_disposed = partialmethod(Events_CallbackHandler.on, CxnEvent.DISPOSED)
    on_login_success = partialmethod(Events_CallbackHandler.on, CxnEvent.LOGIN_SUCCESS)
    on_login_fail = partialmethod(Events_CallbackHandler.on, CxnEvent.LOGIN_FAIL)
    off_connecting = partialmethod(Events_CallbackHandler.off, CxnEvent.CONNECTING)
    off_connected = partialmethod(Events_CallbackHandler.off, CxnEvent.CONNECTED)
    off_reconnecting = partialmethod(Events_CallbackHandler.off, CxnEvent.RECONNECTING)
    off_reconnected = partialmethod(Events_CallbackHandler.off, CxnEvent.RECONNECTED)
    off_disconnecting = partialmethod(Events_CallbackHandler.off, CxnEvent.DISCONNECTING)
    off_disconnected = partialmethod(Events_CallbackHandler.off, CxnEvent.DISCONNECTED)
    off_disposed = partialmethod(Events_CallbackHandler.off, CxnEvent.DISPOSED)
    off_login_success = partialmethod(Events_CallbackHandler.off, CxnEvent.LOGIN_SUCCESS)
    off_login_fail = partialmethod(Events_CallbackHandler.off, CxnEvent.LOGIN_FAIL)
    dispatch_connecting = partialmethod(Events_CallbackHandler.dispatch, CxnEvent.CONNECTING)
    dispatch_connected = partialmethod(Events_CallbackHandler.dispatch, CxnEvent.CONNECTED)
    dispatch_reconnecting = partialmethod(Events_CallbackHandler.dispatch, CxnEvent.RECONNECTING)
    dispatch_reconnected = partialmethod(Events_CallbackHandler.dispatch, CxnEvent.RECONNECTED)
    dispatch_disconnecting = partialmethod(Events_CallbackHandler.dispatch, CxnEvent.DISCONNECTING)
    dispatch_disconnected = partialmethod(Events_CallbackHandler.dispatch, CxnEvent.DISCONNECTED)
    dispatch_disposed = partialmethod(Events_CallbackHandler.dispatch, CxnEvent.DISPOSED)
    dispatch_login_success = partialmethod(dispatch_msg, CxnEvent.LOGIN_SUCCESS)
    dispatch_login_fail = partialmethod(dispatch_msg, CxnEvent.LOGIN_FAIL)
    dispatch_refresh = partialmethod(dispatch_stream_id, StreamEvtID.REFRESH)
    dispatch_status = partialmethod(dispatch_stream_id, StreamEvtID.STATUS)
    dispatch_complete = partialmethod(dispatch_stream_id, StreamEvtID.COMPLETE)
    dispatch_update = partialmethod(dispatch_stream_id, StreamEvtID.UPDATE)
    dispatch_error = partialmethod(dispatch_stream_id, StreamEvtID.ERROR)
    dispatch_ack = partialmethod(dispatch_stream_id, StreamEvtID.ACK)
    dispatch_alarm = partialmethod(dispatch_stream_id, StreamEvtID.ALARM)
    dispatch_response = partialmethod(dispatch_stream_id, StreamEvtID.RESPONSE)

    def __init__(self, originator) -> None:
        super().__init__(originator)
        self._disposed = False

    def dispose(self):
        if self._disposed:
            return

        self._disposed = True
        self._originator = None

        if self._callback_handler_ is not None:
            self._callback_handler_.remove_all_callbacks()
            self._callback_handler_ = None
