from typing import TYPE_CHECKING, Optional, Union

from refinitiv.data._listener import EventListener, ContextType
from ._cxn_listeners import CxnListeners

if TYPE_CHECKING:
    from .. import StreamConnection
    from ... import _RDPStream  # noqa: F401


class AckRDPListener(EventListener[Union[ContextType, "_RDPStream"]]):
    """
    Listener for ACK EVENT from RDPStreamConnection for _RDPStream class
    """

    message: Optional[dict] = None

    def callback(self, originator: "StreamConnection", message: dict, *args, **kwargs):
        self.message = message
        message_state = message.get("state", {})
        stream_state = message_state.get("context")
        context = self.context
        if stream_state == "Closed":
            context.debug(
                f"{context.classname} received a closing message, ",
                f"message_state={message_state}, state={context.state}",
            )

            if context.is_opening_st:
                context.debug(f"{context.classname} open event is set in {self.classname}")
                context.open_evt.set()

        context.events.dispatch_ack(message)


class AlarmRDPListener(EventListener[Union[ContextType, "_RDPStream"]]):
    """
    Listener for ALARM EVENT from RDPStreamConnection for _RDPStream class
    """

    message: Optional[dict] = None

    def callback(self, originator: "StreamConnection", message: dict, *args, **kwargs):
        """
        {
            "data": [],
            "state": {
                "id": "QPSValuation.ERROR_REQUEST_TIMEOUT",
                "code": 408,
                "status": "ERROR",
                "message": "The request could not be executed
                            within the service allocated time",
                "context": "Open"
            },
            "type": "Alarm",
            "streamID": "3"
        }
        """
        self.message = message
        context = self.context
        context.error(f"{message}")

        if context.is_opening_st:
            context.debug(f"{context.classname} open event is set in {self.classname}")
            context.open_evt.set()

        context.events.dispatch_alarm(message)


class ResponseRDPListener(EventListener[Union[ContextType, "_RDPStream"]]):
    """
    Listener for RESPONSE EVENT from RDPStreamConnection for _RDPStream class
    """

    message: Optional[dict] = None

    def callback(self, originator: "StreamConnection", message: dict, *args, **kwargs):
        self.message = message
        context = self.context
        if context.is_opening_st:
            context.debug(f"{context.classname} open event is set in {self.classname}")
            context.open_evt.set()

        context.events.dispatch_response(message)


class UpdateRDPListener(EventListener[Union[ContextType, "_RDPStream"]]):
    """
    Listener for UPDATE EVENT from RDPStreamConnection for _RDPStream class
    """

    message: Optional[dict] = None

    def callback(self, originator: "StreamConnection", message: dict, *args, **kwargs):
        self.message = message
        self.context.events.dispatch_update(message)


class RDPCxnListeners(CxnListeners):
    """
    Events listeners from RDPStreamConnection for _RDPStream class
    """

    ack_listener_class = AckRDPListener
    alarm_listener_class = AlarmRDPListener
    response_listener_class = ResponseRDPListener
    update_listener_class = UpdateRDPListener

    def __init__(self, stream: "_RDPStream") -> None:
        CxnListeners.__init__(self, stream)
        self.ack = self.ack_listener_class(stream)
        self.alarm = self.alarm_listener_class(stream)
        self.response = self.response_listener_class(stream)
        self.update = self.update_listener_class(stream)
