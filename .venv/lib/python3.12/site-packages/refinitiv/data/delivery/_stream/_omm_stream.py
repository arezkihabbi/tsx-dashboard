import asyncio
import os
from functools import partial
from threading import Event
from typing import Optional, TYPE_CHECKING, Tuple, Callable

from ._contrib_response import ContribResponse, RejectedContribResponse, NullContribResponse
from ._contrib_type import contrib_type_enum_arg_parser, OptContribT
from ._protocol_type import ProtocolType
from ._stream import Stream, update_message_with_extended_params
from ._validator_exceptions import ValidationException, ValidationsException
from .event import StreamEvtID
from .events import OMMStreamEvts, OMMCxnListeners, EventsType, create_events, OnStreamContribCxnListeners
from .states import OMMStreamStates
from ..._tools import cached_property, OrEvent

if TYPE_CHECKING:
    from ..._types import OptStr, ExtendedParams, Strings, OptInt, OptDict
    from ._stream_factory import StreamDetails
    from ..._core.session import Session


class _OMMStream(Stream):
    contrib_response: Optional[ContribResponse] = None
    post_user_info: "OptDict" = None

    _post_id: "OptInt" = None

    def __init__(
        self,
        stream_id: int,
        session: "Session",
        name: str,
        details: "StreamDetails",
        domain: str = "MarketPrice",
        service: "OptStr" = None,
        fields: Optional["Strings"] = None,
        key: Optional[dict] = None,
        extended_params: "ExtendedParams" = None,
        owner=None,
        events_type: EventsType = EventsType.OMM_ORIGINATOR_MESSAGE,
    ) -> None:
        if not hasattr(self, "classname"):
            self.classname = (
                f"{self.__class__.__name__} id={stream_id} name='{name}'"  # should be before Stream.__init__
            )

        Stream.__init__(self, stream_id, session, details)
        self._name = name
        self._service = service
        self._fields = fields
        self._domain = domain
        self._key = key
        self._extended_params = extended_params
        self.with_updates: bool = True
        self.is_complete = False
        self.refresh_event_id = stream_id + StreamEvtID.REFRESH
        self.update_event_id = stream_id + StreamEvtID.UPDATE
        self.status_event_id = stream_id + StreamEvtID.STATUS
        self.complete_event_id = stream_id + StreamEvtID.COMPLETE
        self.error_event_id = stream_id + StreamEvtID.ERROR
        self.ack_event_id = stream_id + StreamEvtID.ACK
        self.owner = owner
        self.events_type = events_type

    @cached_property
    def error_evt(self) -> Event:
        return Event()

    @cached_property
    def ack_evt(self) -> Event:
        return Event()

    @cached_property
    def contributed(self) -> OrEvent:
        return OrEvent(self.error_evt, self.ack_evt)

    @cached_property
    def states(self) -> OMMStreamStates:
        return OMMStreamStates(self)

    @cached_property
    def events(self) -> OMMStreamEvts:
        return create_events(self.events_type, self, self.owner)

    @cached_property
    def cxn_listeners(self) -> OMMCxnListeners:
        return OMMCxnListeners(self)

    @cached_property
    def contrib_listeners(self) -> OMMCxnListeners:
        return OnStreamContribCxnListeners(self)

    def on_ack(self, callback: Callable) -> OMMStreamEvts:
        return self.events.on_ack(callback)

    def on_complete(self, callback: Callable) -> OMMStreamEvts:
        return self.events.on_complete(callback)

    def on_error(self, callback: Callable) -> OMMStreamEvts:
        return self.events.on_error(callback)

    def on_refresh(self, callback: Callable) -> OMMStreamEvts:
        return self.events.on_refresh(callback)

    def on_status(self, callback: Callable) -> OMMStreamEvts:
        return self.events.on_status(callback)

    def on_update(self, callback: Callable) -> OMMStreamEvts:
        return self.events.on_update(callback)

    def off_ack(self):
        self.events.off_ack()

    def off_complete(self):
        self.events.off_complete()

    def off_error(self):
        self.events.off_error()

    def off_refresh(self):
        self.events.off_refresh()

    def off_status(self):
        self.events.off_status()

    def off_update(self):
        self.events.off_update()

    @property
    def post_id(self) -> int:
        return self._post_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def protocol_type(self) -> ProtocolType:
        return ProtocolType.OMM

    @property
    def domain(self) -> str:
        return self._domain

    @property
    def refresh_stream_state(self) -> str:
        return self.cxn_listeners.refresh.stream_state

    @property
    def refresh_message_state(self) -> str:
        return self.cxn_listeners.refresh.message_state

    @property
    def status_stream_state(self) -> str:
        return self.cxn_listeners.status.stream_state

    @property
    def status_message_state(self) -> str:
        return self.cxn_listeners.status.message_state

    @property
    def service(self):
        return self._service

    @property
    def open_message(self):
        msg = {
            "ID": self.id,
            "Domain": self._domain,
            "Streaming": self.with_updates,
            "Key": {},
        }

        if self._key:
            msg["Key"] = self._key

        msg["Key"]["Name"] = self.name

        if self.service:
            msg["Key"]["Service"] = self.service

        if self._fields:
            msg["View"] = self._fields

        if self._extended_params:
            msg = update_message_with_extended_params(msg, self._extended_params)

        return msg

    @cached_property
    def close_message(self):
        return {"ID": self.id, "Type": "Close"}

    def send_open_message(self):
        self.send(self.open_message)

    def get_contrib_message(self, fields: dict, contrib_type: OptContribT) -> dict:
        message = {
            "Ack": True,
            "ID": self.id,
            "Message": {
                "Fields": fields,
                "ID": self.id,
                "Type": contrib_type_enum_arg_parser.get_str(contrib_type if contrib_type else "Update"),
                "Domain": self.domain,
            },
            "PostID": self.post_id,
            "Type": "Post",
            "Domain": self.domain,
        }

        post_user_info = self.post_user_info
        if not post_user_info:
            ip, _ = self.cxn.get_socket_info()
            post_user_info = {"Address": ip, "UserID": os.getpid()}

        message["PostUserInfo"] = post_user_info

        return message

    def get_contrib_error_message(self) -> dict:
        return {
            "Type": "Error",
            "Message": "Contribute failed because of disconnection.",
        }

    def set_post_id(self):
        """
        For onstream contrib, the post id is a new one
        """
        self._post_id = self.session._get_omm_stream_id()

    def validate_fields(self, fields: dict) -> Tuple[bool, dict]:
        is_valid = True
        config = self.session.config
        is_field_validation = config.get(f"{self.cxn.api_cfg_key}.contrib.field-validation")

        if is_field_validation:
            endpoints_key, _ = self.cxn.api_cfg_key.rsplit(".", 1)
            api = None
            counter = 0
            for endpoint in config.get(endpoints_key):
                metadata_download = config.get(f"{endpoints_key}.{endpoint}.metadata.download")
                if metadata_download:
                    api = f"{endpoints_key}.{endpoint}"
                    counter += 1

            if api is None or counter == 0:
                raise ValueError(f"Cannot find metadata download api in config")

            if counter > 1:
                raise ValueError(f"More than one metadata download api in config")

            self.session._load_metadata(api=api)

            error = None
            try:
                fields = self.session._validate_metadata(fields)
            except ValidationException as e:
                error = {"Text": e.value}
            except ValidationsException as e:
                error = e.invalid

            if error:
                is_valid = False
                self.contrib_response = RejectedContribResponse(error)

        return is_valid, fields

    def contribute(
        self, fields: dict, contrib_type: OptContribT = None, post_user_info: "OptDict" = None
    ) -> ContribResponse:
        return self.state.contribute(fields, contrib_type, post_user_info)

    async def contribute_async(
        self, fields: dict, contrib_type: OptContribT = None, post_user_info: "OptDict" = None
    ) -> ContribResponse:
        return await asyncio.get_event_loop().run_in_executor(
            None, partial(self.contribute, fields, contrib_type, post_user_info)
        )

    def do_contribute(
        self,
        fields: dict,
        contrib_type: OptContribT = None,
        post_user_info: "OptDict" = None,
    ) -> "ContribResponse":
        self.transition_to(self.states.contributing_st)
        self.set_post_id()
        self.post_user_info = post_user_info
        self.error_evt.clear()
        self.ack_evt.clear()
        self.contrib_response = NullContribResponse()
        is_valid, fields = self.validate_fields(fields)

        if is_valid:
            sent = self.send(self.get_contrib_message(fields, contrib_type))

            if sent:
                self.contributed.wait()

                if self.is_close_st:
                    self.events.dispatch_error(self.get_contrib_error_message())

        else:
            self.error(
                f"{self.classname} Contribute failure caused by fields validation, " f"error={self.contrib_response}"
            )

        self.transition_to(self.states.open_st)

        return self.contrib_response

    def _do_open(self, *args, with_updates=True, **kwargs) -> None:
        self.with_updates = with_updates
        super()._do_open(*args, **kwargs)

    def _do_close(self, *args, **kwargs) -> None:
        self.contributed.set()
        super()._do_close(*args, **kwargs)

    def on_cxn_listeners(self, listeners: "OMMCxnListeners") -> None:
        super().on_cxn_listeners(listeners)
        cxn_events = self.cxn.events
        cxn_events.on(self.ack_event_id, listeners.ack)
        cxn_events.on(self.complete_event_id, listeners.complete)
        cxn_events.on(self.error_event_id, listeners.error)
        cxn_events.on(self.refresh_event_id, listeners.refresh)
        cxn_events.on(self.status_event_id, listeners.status)
        cxn_events.on(self.update_event_id, listeners.update)

    def off_cxn_listeners(self, listeners: "OMMCxnListeners") -> None:
        cxn_events = self.cxn.events
        cxn_events.off(self.ack_event_id, listeners.ack)
        cxn_events.off(self.complete_event_id, listeners.complete)
        cxn_events.off(self.error_event_id, listeners.error)
        cxn_events.off(self.refresh_event_id, listeners.refresh)
        cxn_events.off(self.status_event_id, listeners.status)
        cxn_events.off(self.update_event_id, listeners.update)
        super().off_cxn_listeners(listeners)
