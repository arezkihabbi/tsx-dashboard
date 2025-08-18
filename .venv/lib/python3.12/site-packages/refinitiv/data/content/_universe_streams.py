import asyncio
import itertools
import threading
from concurrent.futures import ThreadPoolExecutor, wait
from functools import partial
from typing import TYPE_CHECKING, Union, Iterable, Dict, KeysView, ValuesView, ItemsView, Optional, Callable

import pandas as pd

from ._events import _UniverseStreamsEvts
from ._listeners import UniverseStmListenersUniverseStreams
from ._states import UniverseStreamsStates
from ._universe_stream import _UniverseStream
from .._core.session import DesktopSession
from .._errors import ItemWasNotRequested
from .._tools import (
    universe_arg_parser,
    fields_arg_parser,
    cached_property,
    try_copy_to_list,
    quotes,
    PRICING_DATETIME_PATTERN,
    convert_df_columns_to_datetime_re,
)
from .._types import Strings, OptStr, OptDict
from ..delivery._stream import BaseStream, StreamOpenWithUpdatesMixin, OptContribT, ErrorContribResponse
from ..delivery.omm_stream import ContribResponse

if TYPE_CHECKING:
    from .._listener import EventListener
    from .._core.session import Session
    from .pricing._stream_facade import PricingStream

_id_iterator = itertools.count()


def raise_err_if_exists(futures):
    for fut in futures:
        exception = fut.exception()
        if exception:
            raise exception


def build_df(universe: Strings, fields: Strings, values_by_field: dict, convert: bool) -> pd.DataFrame:
    data = []
    for inst_name in universe:
        items = []

        for values in values_by_field.values():
            item = values.pop(0)

            if item is None:
                item = pd.NA

            items.append(item)

        data.append((inst_name, *items))

    df = pd.DataFrame(data=data, columns=("Instrument", *fields))

    if convert:
        df = df.convert_dtypes()

    convert_df_columns_to_datetime_re(df, PRICING_DATETIME_PATTERN)

    return df


def validate(name, input_values, requested_values):
    input_values = set(input_values)
    requested_values = set(requested_values)
    not_requested = input_values - requested_values
    has_not_requested = bool(not_requested)

    if has_not_requested:
        raise ItemWasNotRequested(name, not_requested, requested_values)


def get_available_fields(value_by_fields_by_inst_names):
    available_fields = []
    for value_by_fields in value_by_fields_by_inst_names.values():
        fields = value_by_fields.keys()
        available_fields.extend(fields)
    return list(dict.fromkeys(available_fields))


class UniverseStreamFacade(StreamOpenWithUpdatesMixin):
    def __init__(self, stream: _UniverseStream):
        self._stream: _UniverseStream = stream

    @property
    def id(self) -> int:
        return self._stream.id

    @property
    def code(self):
        return self._stream.status_stream_state

    @property
    def message(self):
        return self._stream.status_message_state

    @property
    def name(self):
        return self._stream.name

    @property
    def service(self):
        return self._stream.service

    @property
    def fields(self):
        return self._stream.fields

    @property
    def status(self):
        return self._stream.status

    @property
    def is_ok(self):
        return self._stream.is_ok

    def __enter__(self):
        return self._stream.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._stream.__exit__(exc_type, exc_val, exc_tb)

    def get_field_value(self, field):
        return self._stream.get_field_value(field)

    def get_fields(self, fields=None) -> dict:
        return self._stream.get_fields(fields)

    def keys(self):
        return self._stream.keys()

    def values(self):
        return self._stream.values()

    def items(self):
        return self._stream.items()

    def __iter__(self):
        return self._stream.__iter__()

    def __getitem__(self, field):
        try:
            item = self._stream.__getitem__(field)
        except KeyError:
            item = None
        return item

    def __len__(self):
        return self._stream.__len__()

    def __repr__(self):
        return self._stream.__repr__()

    def __str__(self):
        return self._stream.__str__()


class _UniverseStreams(BaseStream["UniverseStreamsSt"]):
    def __init__(
        self,
        content_type,
        universe: Union[str, Iterable[str]],
        session: "Session",
        item_facade_class=UniverseStreamFacade,
        fields: Union[str, list] = None,
        service: str = None,
        api: OptStr = None,
        extended_params: dict = None,
        owner=None,
    ) -> None:
        stream_id = next(_id_iterator)
        self.classname = f"{self.__class__.__name__} id={stream_id} universe={quotes(universe)}"  # should be before BaseStream.__init__
        BaseStream.__init__(self, stream_id, session)
        self._universe: Strings = universe_arg_parser.get_list(universe)
        self.fields: Strings = fields_arg_parser.get_list(fields or [])
        self._service = service
        self._api = api
        self._extended_params = extended_params
        self.completed = set()
        self.closed = set()
        self._content_type = content_type
        self._item_facade_class = item_facade_class
        self.lock_insts_fields = threading.Lock()
        self.owner = owner
        self._with_updates = True

    @cached_property
    def states(self) -> UniverseStreamsStates:
        return UniverseStreamsStates(self)

    @cached_property
    def universe_stream_listeners(self) -> UniverseStmListenersUniverseStreams:
        return UniverseStmListenersUniverseStreams(self)

    @cached_property
    def events(self) -> _UniverseStreamsEvts:
        return _UniverseStreamsEvts(self)

    def on_ack(self, callback: Callable):
        self.events.on_ack(callback)

    def on_complete(self, callback: Callable):
        self.events.on_complete(callback)

    def on_error(self, callback: Callable):
        self.events.on_error(callback)

    def on_refresh(self, callback: Union[Callable, "EventListener"]):
        self.events.on_refresh(callback)

    def on_status(self, callback: Callable):
        self.events.on_status(callback)

    def on_update(self, callback: Union[Callable, "EventListener"]):
        self.events.on_update(callback)

    @BaseStream.session.setter
    def session(self, session: "Session"):
        BaseStream.session.fset(self, session)
        for stream in self.streams():
            stream.session = session

    @property
    def universe(self):
        return self._universe

    def create_stream_by_name(self, name) -> _UniverseStream:
        return _UniverseStream(
            content_type=self._content_type,
            name=name,
            session=self.session,
            owner=self,
            fields=self.fields,
            service=self._service,
            api=self._api,
            extended_params=self._extended_params,
        )

    @cached_property
    def stream_by_name(self) -> Dict[str, _UniverseStream]:
        return {name: self.create_stream_by_name(name) for name in self.universe}

    def keys(self) -> KeysView[str]:
        return self.stream_by_name.keys()

    def values(self) -> ValuesView[_UniverseStream]:
        return self.stream_by_name.values()

    def items(self) -> ItemsView[str, _UniverseStream]:
        return self.stream_by_name.items()

    def streams(self) -> ValuesView[_UniverseStream]:
        return self.stream_by_name.values()

    def __iter__(self):
        return StreamIterator(self)

    def __getitem__(self, name) -> Union[_UniverseStream, dict, UniverseStreamFacade, "PricingStream"]:
        stream = self.stream_by_name.get(name, {})

        if stream == {}:
            self.warning(f"'{name}' not in {self.classname} universe")
            return stream

        if hasattr(stream, "_wrapper"):
            wrapper = stream._wrapper
        else:
            wrapper = self._item_facade_class(stream)
            stream._wrapper = wrapper

        return wrapper

    def __len__(self):
        return len(self.stream_by_name)

    def _get_value_by_fields_by_inst_names(self, universe: "Strings", fields: "Strings") -> dict:
        retval = {}
        for name in universe:
            stream = self.stream_by_name.get(name)
            values_by_fields = stream.get_fields(fields)
            if values_by_fields:
                retval[name] = values_by_fields

        return retval

    def get_snapshot(
        self,
        universe: Optional[Union[str, Strings]] = None,
        fields: Optional[Union[str, Strings]] = None,
        convert: bool = True,
    ) -> pd.DataFrame:
        """
        Returns a Dataframe filled with snapshot values
        for a list of instrument names and a list of fields.

        Parameters
        ----------
        universe: list of strings
            List of instruments to request snapshot data on.

        fields: str or list of strings
            List of fields to request.

        convert: boolean
            If True, force numeric conversion for all values.

        Returns
        -------
            pandas.DataFrame

            pandas.DataFrame content:
                - columns : instrument and field names
                - rows : instrument name and field values

        Raises
        ------
            Exception
                If request fails or if server returns an error

            ValueError
                If a parameter type or value is wrong

        """

        if universe:
            universe = try_copy_to_list(universe)
            universe = universe_arg_parser.get_list(universe)
            try:
                validate("Instrument", universe, self.universe)
            except ItemWasNotRequested as e:
                self.error(e)
                return pd.DataFrame()
        else:
            universe = self.universe

        value_by_fields_by_inst_names: dict = self._get_value_by_fields_by_inst_names(universe, fields)

        if fields:
            fields = try_copy_to_list(fields)
            fields = fields_arg_parser.get_unique(fields or [])

            try:
                self.fields and validate("Field", fields, self.fields)
            except ItemWasNotRequested as e:
                self.error(e)
                return pd.DataFrame()
        else:
            fields = get_available_fields(value_by_fields_by_inst_names)

        values_by_field = {
            field: [value_by_fields_by_inst_names.get(name, {}).get(field) for name in universe] for field in fields
        }

        return build_df(universe, fields, values_by_field, convert)

    def contribute(
        self, name: str, fields: dict, contrib_type: OptContribT = None, post_user_info: OptDict = None
    ) -> "ContribResponse":
        return self.state.contribute(name, fields, contrib_type, post_user_info)

    async def contribute_async(
        self, name: str, fields: dict, contrib_type: OptContribT = None, post_user_info: OptDict = None
    ) -> "ContribResponse":
        return await asyncio.get_event_loop().run_in_executor(
            None,
            partial(self.contribute, name, fields, contrib_type, post_user_info),
        )

    def close_open_streams(self):
        self.is_debug() and self.debug(f"{self.classname} close_open_streams")

        def close_open(stream):
            stream.events.off_close()
            stream.close()
            stream.events.on_close(self.universe_stream_listeners.close)
            stream.open(with_updates=self._with_updates)

        with ThreadPoolExecutor(thread_name_prefix="CloseOpenUniverseStreams-Thread") as executor:
            futures = [executor.submit(close_open, stream) for stream in self.streams()]
            wait(futures)
            raise_err_if_exists(futures)

    def streams_send_open_message(self):
        self.is_debug() and self.debug(f"{self.classname} streams_send_open_message")

        with ThreadPoolExecutor(thread_name_prefix="SendOpenMsgUniverseStreams-Thread") as executor:
            futures = [executor.submit(stream.send_open_message) for stream in self.streams()]
            wait(futures)
            raise_err_if_exists(futures)

    def remove_fields_from_record(self, fields):
        self.is_debug() and self.debug(f"{self.classname} remove_fields_from_record fields={fields}")
        for stream in self.streams():
            stream.remove_fields_from_record(fields)

    def add_fields(self, fields) -> None:
        self.is_debug() and self.debug(f"{self.classname} add_fields fields={fields}")
        self.state.add_fields(fields)

    def remove_fields(self, fields) -> None:
        self.is_debug() and self.debug(f"{self.classname} remove_fields fields={fields}")
        self.state.remove_fields(fields)

    def add_instruments(self, instruments) -> None:
        self.is_debug() and self.debug(f"{self.classname} add_instruments instruments={instruments}")
        self.state.add_instruments(instruments)

    def remove_instruments(self, instruments) -> None:
        self.is_debug() and self.debug(f"{self.classname} remove_instruments instruments={instruments}")
        self.state.remove_instruments(instruments)

    def _do_open(self, *args, with_updates=True, **kwargs) -> None:
        self._with_updates = with_updates

        if not self.streams():
            raise ValueError("No instrument to subscribe")

        self.completed.clear()
        self.closed.clear()
        self.open_streams(self.streams())

    def open_streams(self, streams: Iterable[_UniverseStream]):
        self.is_debug() and self.debug(f"{self.classname} start open {[stream.name for stream in streams]}")

        with ThreadPoolExecutor(thread_name_prefix="OpenUniverseStreams-Thread") as executor:
            futures = []
            universe_stream_listeners = self.universe_stream_listeners
            for universe_stream in streams:
                universe_stream_events = universe_stream.events
                universe_stream_events.on_update(universe_stream_listeners.update)
                universe_stream_events.on_ack(universe_stream_listeners.ack)
                universe_stream_events.on_refresh(universe_stream_listeners.refresh)
                universe_stream_events.on_status(universe_stream_listeners.status)
                universe_stream_events.on_complete(universe_stream_listeners.complete)
                universe_stream_events.on_error(universe_stream_listeners.error)
                universe_stream_events.on_close(universe_stream_listeners.close)
                futures.append(executor.submit(universe_stream.open, with_updates=self._with_updates))

            wait(futures)
            raise_err_if_exists(futures)

        self.is_debug() and self.debug(f"{self.classname} end open {[stream.name for stream in streams]}")

    def _do_close(self, *args, **kwargs) -> None:
        self.is_debug() and self.debug(f"{self.classname} start close")

        with ThreadPoolExecutor(thread_name_prefix="CloseUniverseStreams-Thread") as executor:
            futures = []
            for universe_stream in self.values():
                universe_stream_events = universe_stream.events
                universe_stream_events.off_update()
                universe_stream_events.off_ack()
                universe_stream_events.off_refresh()
                universe_stream_events.off_status()
                universe_stream_events.off_complete()
                universe_stream_events.off_error()
                universe_stream_events.off_close()
                futures.append(executor.submit(universe_stream.close))

            wait(futures)
            raise_err_if_exists(futures)

        self.is_debug() and self.debug(f"{self.classname} end close")

    def do_add_fields(self, fields) -> None:
        with self.lock_insts_fields:
            fields = fields_arg_parser.get_list(fields)

            exists_fields = set(fields) & set(self.fields)
            if exists_fields:
                self.error(f"{exists_fields} already in fields list")

            fields = [i for i in fields if i not in self.fields]  # universe should be unique
            if not fields:
                return
            self.fields.extend(fields)

            if self.is_open_st:
                if isinstance(self.session, DesktopSession):
                    self.close_open_streams()

                else:
                    self.streams_send_open_message()

    def do_remove_fields(self, fields) -> None:
        with self.lock_insts_fields:
            fields = fields_arg_parser.get_list(fields)
            not_exists_fields = set(fields) - set(self.fields)
            if not_exists_fields:
                self.error(f"{not_exists_fields} not in fields list")

            fields = [i for i in fields if i in self.fields]
            if not fields:
                return
            for i in fields:
                self.fields.remove(i)

            if self.is_open_st:
                if isinstance(self.session, DesktopSession):
                    self.close_open_streams()

                else:
                    self.streams_send_open_message()

                self.remove_fields_from_record(fields)

    def do_add_instruments(self, instruments) -> None:
        with self.lock_insts_fields:
            instruments = universe_arg_parser.get_list(instruments)

            if self.is_unopened_st:
                # universe update is enough, cache will create when universe_streams open
                self.universe.extend(instruments)

            else:
                new_streams = []
                for instrument in instruments:
                    if instrument in self.universe:
                        self.error(f"{instrument} already in universe list")
                        continue

                    if self.is_unopened_st:
                        self.universe.append(instrument)

                    elif self.is_open_st:
                        new_stream = self.create_stream_by_name(instrument)
                        new_streams.append(new_stream)
                        self.stream_by_name[instrument] = new_stream
                        self.universe.append(instrument)

                    elif self.is_close_st:
                        self.stream_by_name[instrument] = self.create_stream_by_name(instrument)
                        self.universe.append(instrument)

                    else:
                        raise NotImplementedError(f"do_add_instrument for {self.state}")

                self.update_classname()
                new_streams and self.open_streams(new_streams)

    def do_remove_instruments(self, instruments) -> None:
        with self.lock_insts_fields:
            if not self.universe:
                self.error("nothing to delete")
                return

            for instrument in universe_arg_parser.get_list(instruments):
                if instrument not in self.universe:
                    self.error(f"{instrument} not in universe list")
                    continue

                if self.is_unopened_st:
                    self.universe.remove(instrument)

                elif self.is_open_st:
                    self.universe.remove(instrument)
                    self.stream_by_name[instrument].close()
                    del self.stream_by_name[instrument]

                elif self.is_close_st:
                    self.universe.remove(instrument)
                    del self.stream_by_name[instrument]

                else:
                    raise NotImplementedError(f"do_remove_instruments for {self.state}")

            self.update_classname()

    def do_contribute(
        self, name: str, fields: dict, contrib_type: OptContribT = None, post_user_info: OptDict = None
    ) -> "ContribResponse":
        universe_stream = self.stream_by_name.get(name)
        if universe_stream:
            self.is_debug() and self.debug(f"{self.classname} start contribute name={name}")
            contrib_response = universe_stream.contribute(fields, contrib_type, post_user_info)
            self.is_debug() and self.debug(f"{self.classname} end contribute name={name}")
            return contrib_response

        else:
            self.error(f"Can't contribute to unsubscribed item {name}")
            return ErrorContribResponse({"Text": f"Can't contribute to unsubscribed item {name}"})

    def update_classname(self):
        self.classname = f"{self.__class__.__name__} id={self.id} universe={quotes(self.universe)}"


class StreamIterator:
    def __init__(self, stream: _UniverseStreams):
        self._stream = stream
        self._index = 0

    def __next__(self):
        if self._index < len(self._stream.universe):
            result = self._stream[self._stream.universe[self._index]]
            self._index += 1
            return result
        raise StopIteration()
