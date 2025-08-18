from abc import ABC, abstractmethod
from threading import Event
from typing import Optional, TYPE_CHECKING

from ._basestream import BaseStream, StreamStateType
from ._protocol_type import ProtocolType
from ._stream_cxn_cache import stream_cxn_cache
from .events import StreamEvts, CxnListeners
from .states import StreamStates
from ..._errors import ScopeError
from ..._tools import cached_property, lazy_dump

if TYPE_CHECKING:
    from ..._content_type import ContentType
    from .._stream import StreamConnection
    from ..._core.session import Session
    from ._stream_factory import StreamDetails


class Stream(BaseStream[StreamStateType], ABC):
    cxn: Optional["StreamConnection"] = None

    def __init__(self, stream_id: int, session: "Session", details: "StreamDetails") -> None:
        BaseStream.__init__(self, stream_id, session=session)
        self.details = details

    @cached_property
    def states(self) -> StreamStates:
        return StreamStates(self)

    @cached_property
    def events(self) -> StreamEvts:
        return StreamEvts(self)

    @cached_property
    def cxn_listeners(self) -> CxnListeners:
        return CxnListeners(self)

    @cached_property
    def open_evt(self) -> Event:
        return Event()

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    def content_type(self) -> "ContentType":
        return self.details.content_type

    @property
    @abstractmethod
    def protocol_type(self) -> ProtocolType:
        pass

    @property
    @abstractmethod
    def close_message(self) -> dict:
        pass

    @property
    @abstractmethod
    def open_message(self) -> dict:
        pass

    def send(self, message: dict) -> bool:
        self.debug(f"{self.classname} state={self.state} send %s", lazy_dump(message))
        return self.state.send(message)

    def do_send(self, message: dict) -> bool:
        return self.cxn.send_message(message)

    def _do_open(self, *args, **kwargs) -> None:
        self.open_evt.clear()

        try:
            self.debug(f"{self.classname} request cxn")
            self.cxn = stream_cxn_cache.get_cxn(self.session, self.details)
            self.debug(f"{self.classname} received cxn={self.cxn.name}")
        except ScopeError as e:
            self.close()
            raise e

        self.on_cxn_listeners(self.cxn_listeners)

        sent = False
        if not self.is_close_st:
            open_message = self.open_message
            self.debug(f"{self.classname} send open_message %s", lazy_dump(open_message))
            sent = self.cxn.send_message(open_message)

        if not self.is_close_st and (self.cxn and not self.cxn.is_disposed) and sent:
            self.debug(f"{self.classname} wait open event")
            self.open_evt.wait()

    def _do_close(self, *args, **kwargs) -> None:
        self.open_evt.set()

        if self.cxn:
            close_message = self.close_message
            self.debug(f"{self.classname} send close_message %s", lazy_dump(close_message))
            self.cxn.send_message(close_message)
            self.off_cxn_listeners(self.cxn_listeners)
            self.debug(f"{self.classname} release cxn={self.cxn.name}")
            stream_cxn_cache.release(self.session, self.details)
            self.cxn = None

    def on_cxn_listeners(self, listeners: "CxnListeners") -> None:
        cxn_events = self.cxn.events
        cxn_events.on_disconnecting(listeners.disconnecting)
        cxn_events.on_reconnected(listeners.reconnected)
        cxn_events.on_disposed(listeners.disposed)

    def off_cxn_listeners(self, listeners: "CxnListeners") -> None:
        cxn_events = self.cxn.events
        cxn_events.off_disconnecting(listeners.disconnecting)
        cxn_events.off_reconnected(listeners.reconnected)
        cxn_events.off_disposed(listeners.disposed)


def update_message_with_extended_params(message: dict, extended_params: dict) -> dict:
    return update_key_in_dict(message, extended_params)


def update_key_in_dict(message: dict, extended_params: dict) -> dict:
    for param, extended_val in extended_params.items():
        if param in message:
            prev_value = message[param]
            if isinstance(prev_value, dict) and isinstance(extended_val, dict):
                update_key_in_dict(prev_value, extended_val)
            else:
                message[param] = extended_val
        else:
            message[param] = extended_val

    return message
