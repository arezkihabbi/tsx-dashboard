import itertools
from threading import Event
from typing import Dict, List, TYPE_CHECKING, Tuple, Callable

from ._chain_record import ChainRecord
from ._display_template import disp_tmpl_to_num_summary_links
from ._events import StreamingChainEvts
from ._listeners import StreamingChainListeners
from ...._content_type import ContentType
from ...._tools import cached_property
from ...._types import ExtendedParams, OptBool, OptInt, OptStr, OptList
from ....delivery._stream import BaseStream, _OMMStream, get_service_and_details_omm

if TYPE_CHECKING:
    from ._stream_facade import Stream
    from ...._core.session import Session

_id_iterator = itertools.count()


class StreamingChain(BaseStream):
    constituents: OptList = None
    display_template: OptInt = None

    def __init__(
        self,
        name: str,
        session: "Session",
        service: OptStr = None,
        skip_summary_links: bool = True,
        skip_empty: OptBool = True,
        override_summary_links: OptInt = None,
        api: OptStr = None,
        extended_params: ExtendedParams = None,
        owner: "Stream" = None,
    ):
        stream_id = next(_id_iterator)
        self.classname = f"{self.__class__.__name__} id={stream_id} name='{name}'"
        BaseStream.__init__(self, stream_id, session)
        self.owner = owner
        self.name: str = name
        self._service = service
        self._skip_summary_links = skip_summary_links
        self._skip_empty = skip_empty
        self._override_summary_links = override_summary_links
        self._api = api
        self.extended_params = extended_params
        self.stream_by_name: Dict[str, _OMMStream] = {}
        self.records_by_name: Dict[str, ChainRecord] = {}
        self.refresh_evt_by_name: Dict[str, Event] = {}
        self.complete_evt: Event = Event()
        self.chain_record_name_to_offset: Dict[str, int] = {self.name: 0}
        self.update_messages: List[Tuple[str, dict]] = []

    @cached_property
    def stream_listeners(self) -> StreamingChainListeners:
        return StreamingChainListeners(self)

    @cached_property
    def events(self) -> StreamingChainEvts:
        return StreamingChainEvts(self)

    def on_ack(self, callback: Callable):
        self.events.on_ack(callback)

    def on_complete(self, callback: Callable):
        self.events.on_complete(callback)

    def on_error(self, callback: Callable):
        self.events.on_error(callback)

    def on_refresh(self, callback: Callable):
        self.events.on_refresh(callback)

    def on_status(self, callback: Callable):
        self.events.on_status(callback)

    def on_update(self, callback: Callable):
        self.events.on_update(callback)

    def on_add(self, callback: Callable):
        self.events.on_add(callback)

    def on_remove(self, callback: Callable):
        self.events.on_remove(callback)

    @property
    def is_chain(self) -> bool:
        if self.is_opening_st:
            self.complete_evt.wait()
        return self.has_record(self.name)

    @property
    def num_summary_links(self) -> int:
        if self._override_summary_links:
            return self._override_summary_links
        else:
            return disp_tmpl_to_num_summary_links.get(self.display_template, None)

    @property
    def summary_links(self) -> List[str]:
        if not self.is_chain:
            return []

        summary_links = self.constituents[: self.num_summary_links]
        return [summary_link for summary_link in summary_links if not self._skip_empty or summary_link is not None]

    @property
    def display_name(self) -> str:
        if not self.is_chain:
            return ""

        return self.get_display_name(self.name)

    @BaseStream.session.setter
    def session(self, session: "Session"):
        BaseStream.session.fset(self, session)
        for stream in self.stream_by_name.values():
            stream.session = session

    def add(self, name: str) -> "_OMMStream":
        session = self.session
        service, details = get_service_and_details_omm(ContentType.STREAMING_CHAINS, session, self._service, self._api)
        stream = _OMMStream(
            stream_id=session._get_omm_stream_id(),
            session=session,
            name=name,
            domain="MarketPrice",
            service=service,
            fields=[],
            extended_params=self.extended_params,
            details=details,
        )
        stream.classname = f"{self.classname} [{stream.classname}]"
        stream_listeners = self.stream_listeners
        stream.on_update(stream_listeners.update)
        stream.on_refresh(stream_listeners.refresh)
        stream.on_status(stream_listeners.status)
        stream.on_error(stream_listeners.error)
        self.stream_by_name[name] = stream
        self.refresh_evt_by_name[name] = Event()
        return stream

    def wait_refresh(self, name: str):
        self.refresh_evt_by_name[name].wait()

    def get_record(self, name: str) -> "ChainRecord":
        return self.records_by_name[name]

    def get_stream(self, name: str) -> "_OMMStream":
        return self.stream_by_name[name]

    def has_record(self, name: str) -> bool:
        return name in self.records_by_name

    def has_stream(self, name: str) -> bool:
        return name in self.stream_by_name

    def is_stream_close(self, name: str) -> bool:
        return self.stream_by_name[name].is_close_st

    def get_display_name(self, name: str) -> str:
        return self.records_by_name[name].display_name

    def get_constituents(self) -> List[str]:
        if not self.is_chain:
            return []

        num_summary_links = self.num_summary_links

        if self._skip_summary_links:
            constituents = self.constituents[num_summary_links:]

        else:
            constituents = self.constituents[:]

        return [constituent for constituent in constituents if not self._skip_empty or constituent is not None]

    def append_constituent(self, index: int, constituent: str):
        self.constituents.append(constituent)
        self.events.dispatch_add(constituent, index)

    def remove_constituent(self, index: int, constituent: str):
        self.constituents.pop(index)
        self.events.dispatch_remove(constituent, index)

    def update_constituent(self, index: int, old_constituent: str, new_constituent: str):
        self.constituents[index] = new_constituent
        self.events.dispatch_update(new_constituent, old_constituent, index)

    def process_remaining_update_messages(self):
        while True:
            try:
                (name, message) = self.update_messages.pop(0)
            except IndexError:
                break

            self.update_chain_record(name, message)

    def update_chain_record(self, name: str, message: dict):
        fields = message.get("Fields", [])

        if not self.has_record(name):
            self.warning(f"StreamingChain :: Skipping to update an invalid chain record = {name}.")
            return

        chain_record = self.get_record(name)
        index_to_old_and_new_constituent = chain_record.update(fields)

        offset = self.chain_record_name_to_offset[name]
        for i, (old_c, new_c) in index_to_old_and_new_constituent.items():
            i = offset + i

            if old_c and new_c:
                self.update_constituent(i, old_c, new_c)

            elif not old_c and new_c:
                self.append_constituent(i, new_c)

            elif old_c and not new_c:
                self.remove_constituent(i, old_c)

    def _do_open(self, *args, with_updates=True, **kwargs) -> None:
        self.constituents = []
        self.complete_evt.clear()
        offset = 0
        name = self.name
        while name:
            if not self.has_stream(name):
                self.add(name).open(with_updates=with_updates)

            self.wait_refresh(name)

            if self.is_stream_close(name):
                break

            if self.has_record(name):
                chain_record = self.get_record(name)
                name = chain_record.next_chain_record_name

                for i, constituent in enumerate(chain_record.constituents):
                    self.append_constituent(offset + i, constituent)

                offset += chain_record.num_constituents or 0

                if name:
                    self.chain_record_name_to_offset[name] = offset

            else:
                break

        self.complete_evt.set()

        self.events.dispatch_complete(self.get_constituents())
        self.process_remaining_update_messages()

    def _do_close(self, *args, **kwargs) -> None:
        for refresh_evt in self.refresh_evt_by_name.values():
            refresh_evt.set()

        for stream in self.stream_by_name.values():
            stream.events.off_all_events()
            stream.close()
