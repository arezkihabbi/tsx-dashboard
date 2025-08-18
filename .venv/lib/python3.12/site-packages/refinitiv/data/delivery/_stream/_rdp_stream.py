from typing import TYPE_CHECKING, Callable

from ._protocol_type import ProtocolType
from ._stream import Stream, update_message_with_extended_params
from ._stream_factory import get_service_and_details_rdp
from .event import StreamEvtID
from .events import RDPStreamEvts, RDPCxnListeners, EventsType, create_events
from ..._content_type import ContentType
from ..._tools import cached_property

if TYPE_CHECKING:
    from ..._types import ExtendedParams
    from ..._core.session import Session


class _RDPStream(Stream):
    def __init__(
        self,
        session: "Session",
        universe: list,
        view: list,
        service: str = "",
        api: str = "",
        parameters: dict = None,
        extended_params: "ExtendedParams" = None,
        owner=None,
        events_type=EventsType.RDP_ORIGINATOR_MESSAGE,
        content_type: ContentType = ContentType.STREAMING_RDP,
    ):
        service, details = get_service_and_details_rdp(content_type, session, service, api)
        stream_id = session._get_rdp_stream_id()
        Stream.__init__(self, stream_id, session, details)
        self._service = service
        self._universe = universe
        self._view = view
        self._parameters = parameters
        self._extended_params = extended_params
        self.ack_event_id = stream_id + StreamEvtID.ACK
        self.alarm_event_id = stream_id + StreamEvtID.ALARM
        self.response_event_id = stream_id + StreamEvtID.RESPONSE
        self.update_event_id = stream_id + StreamEvtID.UPDATE
        self.owner = owner
        self.events_type = events_type

    @cached_property
    def events(self) -> RDPStreamEvts:
        return create_events(self.events_type, self, self.owner)

    @cached_property
    def cxn_listeners(self) -> RDPCxnListeners:
        return RDPCxnListeners(self)

    def on_ack(self, callback: Callable):
        self.events.on_ack(callback)

    def on_alarm(self, callback: Callable):
        self.events.on_alarm(callback)

    def on_response(self, callback: Callable):
        self.events.on_response(callback)

    def on_update(self, callback: Callable):
        self.events.on_update(callback)

    @property
    def service(self) -> str:
        return self._service

    @property
    def universe(self) -> list:
        return self._universe

    @property
    def view(self) -> list:
        return self._view

    @property
    def parameters(self) -> dict:
        return self._parameters

    @property
    def extended_params(self) -> "ExtendedParams":
        return self._extended_params

    @property
    def name(self) -> str:
        return str(self._universe)

    @property
    def protocol_type(self) -> ProtocolType:
        return ProtocolType.RDP

    @cached_property
    def close_message(self):
        return {"streamID": f"{self.id:d}", "method": "Close"}

    @cached_property
    def open_message(self) -> dict:
        message = {
            "streamID": f"{self.id:d}",
            "method": "Subscribe",
            "universe": self.universe,
        }

        if self.service is not None:
            message["service"] = self.service

        if self.view is not None:
            message["view"] = self.view

        if self.parameters is not None:
            message["parameters"] = self.parameters

        if self.extended_params:
            message = update_message_with_extended_params(message, self.extended_params)

        return message

    def on_cxn_listeners(self, listeners: "RDPCxnListeners") -> None:
        super().on_cxn_listeners(listeners)
        cxn_events = self.cxn.events
        cxn_events.on(self.ack_event_id, listeners.ack)
        cxn_events.on(self.alarm_event_id, listeners.alarm)
        cxn_events.on(self.response_event_id, listeners.response)
        cxn_events.on(self.update_event_id, listeners.update)

    def off_cxn_listeners(self, listeners: "RDPCxnListeners") -> None:
        cxn_events = self.cxn.events
        cxn_events.off(self.ack_event_id, listeners.ack)
        cxn_events.off(self.alarm_event_id, listeners.alarm)
        cxn_events.off(self.response_event_id, listeners.response)
        cxn_events.off(self.update_event_id, listeners.update)
        super().off_cxn_listeners(listeners)
