import warnings
from typing import Optional, Union
from typing import TYPE_CHECKING

from ._cxn_listeners import CxnListeners
from .._contrib_response import AckContribResponse, ErrorContribResponse
from ...._listener import EventListener, ContextType

if TYPE_CHECKING:
    from ..._stream import _OMMStream
    from .. import StreamConnection


class ContribAckOMMListener(EventListener[Union[ContextType, "_OMMStream"]]):
    """
    Listener for ACK EVENT from OMMStreamConnection when contribution occurs for _OMMStream class
    """

    message: Optional[dict] = None

    def callback(self, originator: "StreamConnection", message: dict, *args, **kwargs):
        self.message = message
        context = self.context
        context.contrib_response = AckContribResponse(message)
        ack_id = message.get("AckID")
        nack_code = message.get("NakCode")

        if ack_id != context.post_id:
            context.error(
                f"{context.classname} Received Ack message with wrong AckID, "
                f"ack_id={ack_id} != post_id={context.post_id}"
            )

        else:
            if nack_code:
                context.error(
                    f"{context.classname} Received Ack message with NakCode, "
                    f"AckID={ack_id}, NackCode={nack_code}, Text={message.get('Text')}"
                )

        context.ack_evt.set()
        context.events.dispatch_ack(message)


class AckOMMListener(EventListener[Union[ContextType, "_OMMStream"]]):
    """
    Listener for ACK EVENT from OMMStreamConnection for _OMMStream class
    """

    message: Optional[dict] = None

    def callback(self, originator: "StreamConnection", message: dict, *args, **kwargs):
        self.message = message
        self.context.events.dispatch_ack(message)


class CompleteOMMListener(EventListener[Union[ContextType, "_OMMStream"]]):
    """
    Listener for COMPLETE EVENT from OMMStreamConnection for _OMMStream class
    """

    message: Optional[dict] = None

    def callback(self, originator: "StreamConnection", message: dict, *args, **kwargs):
        self.message = message
        context = self.context
        if not context.is_complete:
            context.is_complete = True
            context.events.dispatch_complete(message)

        if context.is_opening_st:
            context.debug(f"{context.classname} open event is set in {self.classname}")
            context.open_evt.set()


class ContribErrorOMMListener(EventListener[Union[ContextType, "_OMMStream"]]):
    """
    Listener for ERROR EVENT from OMMStreamConnection when contribution occurs for _OMMStream class
    """

    message: Optional[dict] = None

    def callback(self, originator: "StreamConnection", message: dict, *args, **kwargs):
        self.message = message
        context = self.context
        context.contrib_response = ErrorContribResponse(message)
        context.error_evt.set()
        context.open_evt.set()
        context.events.dispatch_error(message)


class ErrorOMMListener(EventListener[Union[ContextType, "_OMMStream"]]):
    """
    Listener for ERROR EVENT from OMMStreamConnection for _OMMStream class
    """

    message: Optional[dict] = None

    def callback(self, originator: "StreamConnection", message: dict, *args, **kwargs):
        self.message = message
        self.context.events.dispatch_error(message)


class RefreshOMMListener(EventListener[Union[ContextType, "_OMMStream"]]):
    """
    Listener for REFRESH EVENT from OMMStreamConnection for _OMMStream class
    """

    message: Optional[dict] = None

    stream_state: Optional[str] = None
    message_state: Optional[str] = None

    def callback(self, originator: "StreamConnection", message: dict, *args, **kwargs):
        self.message = message
        message_state = message.get("State", {})
        self.stream_state = message_state.get("Stream", "")
        self.message_state = message_state.get("Text", "")
        self.context.events.dispatch_refresh(message)


class StatusOMMListener(EventListener[Union[ContextType, "_OMMStream"]]):
    """
    Listener for STATUS EVENT from OMMStreamConnection for _OMMStream class
    """

    message: Optional[dict] = None

    stream_state: Optional[str] = None
    message_state: Optional[str] = None

    def callback(self, originator: "StreamConnection", message: dict, *args, **kwargs):
        self.message = message
        context = self.context
        message_state = message.get("State", {})
        stream_state = message_state.get("Stream", "")
        self.stream_state = stream_state
        self.message_state = message_state.get("Text", "")

        if stream_state == "Closed":
            if message_state.get("Code") == "AlreadyOpen":
                warnings.warn(
                    f"{context.classname}|{context.name} received a Closed message: {message_state.get('Text')}",
                )
                context.warning(
                    f"{context.classname} | {context.name} received a Closed message, message_state={message_state}"
                )

            if context.is_opening_st:
                context.debug(f"{context.classname} open event is set in {self.classname}")
                context.open_evt.set()

        context.events.dispatch_status(message)

        if context.is_open_st or context.is_opening_st and not context.is_complete:
            context.is_complete = True
            context.events.dispatch_complete(message)
            context.debug(f"{context.classname} open event is set in {self.classname}")
            context.open_evt.set()


class UpdateOMMListener(EventListener[Union[ContextType, "_OMMStream"]]):
    """
    Listener for UPDATE EVENT from OMMStreamConnection for _OMMStream class
    """

    message: Optional[dict] = None

    def callback(self, originator: "StreamConnection", message: dict, *args, **kwargs):
        self.message = message
        self.context.events.dispatch_update(message)


class OMMCxnListeners(CxnListeners):
    """
    Events listeners from OMMStreamConnection for _OMMStream class
    """

    ack_listener_class = AckOMMListener
    complete_listener_class = CompleteOMMListener
    error_listener_class = ErrorOMMListener
    refresh_listener_class = RefreshOMMListener
    status_listener_class = StatusOMMListener
    update_listener_class = UpdateOMMListener

    def __init__(self, stream: "_OMMStream") -> None:
        CxnListeners.__init__(self, stream)
        self.ack = self.ack_listener_class(stream)
        self.complete = self.complete_listener_class(stream)
        self.error = self.error_listener_class(stream)
        self.refresh = self.refresh_listener_class(stream)
        self.status = self.status_listener_class(stream)
        self.update = self.update_listener_class(stream)


class OnStreamContribCxnListeners(OMMCxnListeners):
    ack_listener_class = ContribAckOMMListener
    error_listener_class = ContribErrorOMMListener
