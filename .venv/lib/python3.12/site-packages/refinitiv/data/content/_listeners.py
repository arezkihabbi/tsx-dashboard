from typing import TYPE_CHECKING

from .._listener import EventListener
from ..delivery._stream.events import OMMCxnListeners, RefreshOMMListener, StatusOMMListener, UpdateOMMListener

if TYPE_CHECKING:
    from ..delivery._stream import StreamConnection
    from ._universe_stream import _UniverseStream
    from ._universe_streams import _UniverseStreams


# --------------------------------------------------------------------------------
# Universe Stream
# --------------------------------------------------------------------------------


class RefreshOMMListenerUniverseStm(RefreshOMMListener["_UniverseStream"]):
    """
    Listener for REFRESH EVENT from OMMStreamConnection for _UniverseStream class
    """

    def callback(self, originator: "StreamConnection", message: dict, *args, **kwargs):
        self.message = message
        message_state = message.get("State", {})
        self.stream_state = message_state.get("Stream", "")
        self.message_state = message_state.get("Text", "")

        context = self.context
        if context.prv_fields:
            message["Fields"] = context.filter_fields(message.get("Fields"))

        context._record = message

        self.context.events.dispatch_refresh(message.get("Fields"))


class StatusOMMListenerUniverseStm(StatusOMMListener["_UniverseStream"]):
    """
    Listener for STATUS EVENT from OMMStreamConnection for _UniverseStream class
    """

    def callback(self, originator: "StreamConnection", message: dict, *args, **kwargs):
        self.context._status = message
        super().callback(originator, message, *args, **kwargs)


class UpdateOMMListenerUniverseStm(UpdateOMMListener["_UniverseStream"]):
    """
    Listener for UPDATE EVENT from OMMStreamConnection for _UniverseStream class
    """

    def callback(self, originator: "StreamConnection", message: dict, *args, **kwargs):
        self.message = message
        self.context.write_to_record(message)
        self.context.events.dispatch_update(message.get("Fields"))


class OMMListenersUniverseStm(OMMCxnListeners):
    refresh_listener_class = RefreshOMMListenerUniverseStm
    status_listener_class = StatusOMMListenerUniverseStm
    update_listener_class = UpdateOMMListenerUniverseStm


# --------------------------------------------------------------------------------
# Universe Streams
# --------------------------------------------------------------------------------


class AckUniverseStmListenerUniverseStreams(EventListener["_UniverseStreams"]):
    """
    Listener for ACK EVENT from _UniverseStream for _UniverseStreams class
    """

    def callback(self, originator: "_UniverseStream", message: dict, *args, **kwargs):
        self.context.events.dispatch_ack(message, originator)


class CompleteUniverseStmListenerUniverseStreams(EventListener["_UniverseStreams"]):
    """
    Listener for COMPLETE EVENT from _UniverseStream for _UniverseStreams class
    """

    def callback(self, originator: "_UniverseStream", message: dict, *args, **kwargs):
        context = self.context
        name = originator.name
        if name not in context.completed:
            context.completed.update([name])
            if context.completed == set(context.universe):
                # received complete event from all streams all, emit global complete
                context.events.dispatch_complete(message)


class ErrorUniverseStmListenerUniverseStreams(EventListener["_UniverseStreams"]):
    """
    Listener for ERROR EVENT from _UniverseStream for _UniverseStreams class
    """

    def callback(self, originator: "_UniverseStream", message: dict, *args, **kwargs):
        self.context.events.dispatch_error(message, originator)


class RefreshUniverseStmListenerUniverseStreams(EventListener["_UniverseStreams"]):
    """
    Listener for REFRESH EVENT from _UniverseStream for _UniverseStreams class
    """

    def callback(self, originator: "_UniverseStream", message: dict, *args, **kwargs):
        self.context.events.dispatch_refresh(message, originator)


class StatusUniverseStmListenerUniverseStreams(EventListener["_UniverseStreams"]):
    """
    Listener for STATUS EVENT from _UniverseStream for _UniverseStreams class
    """

    def callback(self, originator: "_UniverseStream", message: dict, *args, **kwargs):
        context = self.context
        context.events.dispatch_status(message, originator)

        if originator.is_close_st:
            context.events.dispatch_complete(message)


class UpdateUniverseStmListenerUniverseStreams(EventListener["_UniverseStreams"]):
    """
    Listener for UPDATE EVENT from _UniverseStream for _UniverseStreams class
    """

    def callback(self, originator: "_UniverseStream", message: dict, *args, **kwargs):
        self.context.events.dispatch_update(message, originator)


class CloseUniverseStmListenerUniverseStreams(EventListener["_UniverseStreams"]):
    """
    Listener for UPDATE EVENT from _UniverseStream for _UniverseStreams class
    """

    def callback(self, originator: "_UniverseStream", *args, **kwargs):
        name = originator.name
        context = self.context
        if name not in context.closed:
            context.closed.update([name])
            if context.closed == set(context.universe):
                # received close event from all streams, close the universe streams
                context.close()


class UniverseStmListenersUniverseStreams(OMMCxnListeners):
    ack_listener_class = AckUniverseStmListenerUniverseStreams
    complete_listener_class = CompleteUniverseStmListenerUniverseStreams
    error_listener_class = ErrorUniverseStmListenerUniverseStreams
    refresh_listener_class = RefreshUniverseStmListenerUniverseStreams
    status_listener_class = StatusUniverseStmListenerUniverseStreams
    update_listener_class = UpdateUniverseStmListenerUniverseStreams
    close_listener_class = CloseUniverseStmListenerUniverseStreams

    def __init__(self, stream: "_UniverseStreams") -> None:
        super().__init__(stream)
        self.close = self.close_listener_class(stream)
