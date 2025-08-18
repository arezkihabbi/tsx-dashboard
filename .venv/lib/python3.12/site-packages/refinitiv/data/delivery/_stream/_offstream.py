from typing import TYPE_CHECKING

from ._stream_cxn_cache import stream_cxn_cache
from ._contrib_type import contrib_type_enum_arg_parser, OptContribT
from ._omm_stream import _OMMStream
from .events import OffStreamContribCxnListeners, EventsType
from .stream_connection import LOGIN_STREAM_ID
from ..._errors import ScopeError
from ..._tools import cached_property

if TYPE_CHECKING:
    from ._stream_factory import StreamDetails
    from ..._core.session import Session


class _OffStreamContrib(_OMMStream):
    def __init__(
        self,
        stream_id: int,
        session: "Session",
        name: str,
        details: "StreamDetails",
        service: str,
        domain: str,
    ) -> None:
        super().__init__(
            stream_id=stream_id,
            session=session,
            name=name,
            details=details,
            domain=domain,
            service=service,
            owner=self,
            events_type=EventsType.OMM_MESSAGE_ORIGINATOR,
        )
        self._post_id = stream_id

    @cached_property
    def cxn_listeners(self) -> OffStreamContribCxnListeners:
        return OffStreamContribCxnListeners(self)

    def set_post_id(self):
        """
        For offstream contrib, the post id is the same as the stream id
        """
        self._post_id = self.id

    def get_contrib_message(
        self,
        fields: dict,
        contrib_type: OptContribT,
    ) -> dict:
        return {
            "Ack": True,
            "ID": LOGIN_STREAM_ID,
            "Message": {
                "Fields": fields,
                "ID": 0,
                "Type": contrib_type_enum_arg_parser.get_str(contrib_type if contrib_type else "Update"),
                "Domain": self.domain,
            },
            "PostID": self.post_id,
            "Type": "Post",
            "Key": {"Name": self.name, "Service": self.service},
            "Domain": self.domain,
        }

    def _do_open(self, *args, **kwargs):
        try:
            self.debug(f"{self.classname} request cxn")
            self.cxn = stream_cxn_cache.get_cxn(self.session, self.details)
            self.debug(f"{self.classname} received cxn={self.cxn.name}")
        except ScopeError as e:
            self.close()
            raise e

        self.on_cxn_listeners(self.cxn_listeners)

    def _do_close(self, *args, **kwargs):
        self.contributed.set()

        if self.cxn:
            self.off_cxn_listeners(self.cxn_listeners)

            if stream_cxn_cache.has_cxn(self.session, self.details):
                self.debug(f"{self.classname} release cxn={self.cxn.name}")
                stream_cxn_cache.release(self.session, self.details)

            self.cxn = None

    def on_cxn_listeners(self, listeners: "OffStreamContribCxnListeners") -> None:
        cxn_events = self.cxn.events
        cxn_events.on_disconnecting(listeners.disconnecting)
        cxn_events.on_reconnected(listeners.reconnected)
        cxn_events.on_disposed(listeners.disposed)
        cxn_events.on(self.ack_event_id, listeners.ack)
        cxn_events.on(self.error_event_id, listeners.error)

    def off_cxn_listeners(self, listeners: "OffStreamContribCxnListeners") -> None:
        cxn_events = self.cxn.events
        cxn_events.off(self.ack_event_id, listeners.ack)
        cxn_events.off(self.error_event_id, listeners.error)
        cxn_events.off_disconnecting(listeners.disconnecting)
        cxn_events.off_reconnected(listeners.reconnected)
        cxn_events.off_disposed(listeners.disposed)
