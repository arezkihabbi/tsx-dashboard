import asyncio
from contextlib import AbstractContextManager, AbstractAsyncContextManager
from functools import partial
from typing import Optional, Union, TYPE_CHECKING, TypeVar, Generic

from .events import BaseStreamEvts
from .states import BaseStreamStates, BaseStreamState
from ..._core.log_reporter import LogReporter
from ..._core.session import get_default, is_closed
from ..._open_state import OpenState
from ..._tools import cached_property, fill

if TYPE_CHECKING:
    from ..._core.session import Session
    from ...content.ipa.financial_contracts._quantitative_data_stream import QuantitativeDataStream
    from ...content.trade_data_service._stream import TradeDataStream
    from ...content.pricing.chain._stream import StreamingChain
    from ...content._universe_streams import _UniverseStreams
    from . import _OMMStream, _RDPStream

    Stream = Union[
        _UniverseStreams,
        StreamingChain,
        TradeDataStream,
        _RDPStream,
        _OMMStream,
        QuantitativeDataStream,
    ]


class StreamOpenMixin(AbstractContextManager, AbstractAsyncContextManager):
    _stream: "Stream" = None
    _always_use_default_session: bool

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    async def __aenter__(self):
        await self.open_async()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        self.close()

    def _try_update_session(self):
        if self._always_use_default_session:
            self._stream.session = get_default()

    @property
    def open_state(self) -> OpenState:
        return self._stream.state.open_state

    def open(self) -> OpenState:
        self._try_update_session()
        return self._stream.open()

    async def open_async(self) -> OpenState:
        self._try_update_session()
        return await self._stream.open_async()

    def close(self) -> OpenState:
        return self._stream.close()


class StreamOpenWithUpdatesMixin(StreamOpenMixin):
    def open(self, with_updates: bool = True) -> OpenState:
        self._try_update_session()
        self._stream.open(with_updates=with_updates)
        return self.open_state

    async def open_async(self, with_updates: bool = True) -> OpenState:
        self._try_update_session()
        await self._stream.open_async(with_updates=with_updates)
        return self.open_state


StreamStateType = TypeVar("StreamStateType", bound=BaseStreamState)


class TransitionError(AssertionError):
    pass


class BaseStream(Generic[StreamStateType], LogReporter):
    _state: Optional[StreamStateType] = None

    def __init__(self, stream_id: int, session: "Session") -> None:
        if not hasattr(self, "classname"):
            self.classname = f"{self.__class__.__name__} id={stream_id}"

        LogReporter.__init__(self, logger=session.logger())
        self.id: int = stream_id
        self._session: "Session" = session
        self.transition_to(self.states.unopened_st)

    def __repr__(self) -> str:
        return self.classname

    def __str__(self):
        return repr(self)

    def transition_to(self, next_state: StreamStateType):
        prev_state = self.state

        if prev_state == next_state:
            return

        if prev_state:
            if not prev_state.can_transition_to(next_state):
                raise TransitionError(f"Cannot transition from {prev_state} to {next_state}")

            self.debug(f"{self.classname} transition {prev_state} -> {next_state}")
            prev_state.exit()

        self._state = next_state

        next_state.enter()

        if not prev_state:
            self.debug(f"{self.classname} state={next_state} inited")

    @cached_property
    def states(self) -> BaseStreamStates:
        return BaseStreamStates(self)

    @property
    def state(self) -> StreamStateType:
        return self._state

    @property
    def is_unopened_st(self) -> bool:
        return self.state == self.states.unopened_st

    @property
    def is_opening_st(self) -> bool:
        return self.state == self.states.opening_st

    @property
    def is_open_st(self) -> bool:
        return self.state == self.states.open_st

    @property
    def is_close_st(self) -> bool:
        return self.state == self.states.close_st

    @cached_property
    def events(self) -> BaseStreamEvts:
        return BaseStreamEvts(self)

    @property
    def session(self) -> "Session":
        return self._session

    @session.setter
    def session(self, session: "Session"):
        if self._session != session and (self.is_close_st or self.is_unopened_st):
            self._session = session
            LogReporter.__init__(self, logger=self._session.logger())

    def open(self, *args, **kwargs) -> OpenState:
        self.debug(f"{self.classname} state={self.state} open {fill(args=args, kwargs=kwargs)}")
        return self.state.open(*args, **kwargs)

    async def open_async(self, *args, **kwargs) -> OpenState:
        return await asyncio.get_event_loop().run_in_executor(None, partial(self.open, *args, **kwargs))

    def close(self, *args, **kwargs) -> OpenState:
        self.debug(f"{self.classname} state={self.state} close {fill(args=args, kwargs=kwargs)}")
        return self.state.close(*args, **kwargs)

    async def close_async(self, *args, **kwargs) -> OpenState:
        return self.close(*args, **kwargs)

    def do_open(self, *args, **kwargs) -> OpenState:
        if is_closed(self.session):
            raise AssertionError("Session must be open")

        self.transition_to(self.states.opening_st)
        self._do_open(*args, **kwargs)
        if self.is_close_st:
            return OpenState.Closed
        else:
            self.transition_to(self.states.open_st)
            self.events.dispatch_open(self, *args, **kwargs)
            return OpenState.Opened

    def do_close(self, *args, **kwargs) -> OpenState:
        self.transition_to(self.states.close_st)
        self._do_close(*args, **kwargs)
        self.events.dispatch_close(self, *args, **kwargs)
        return OpenState.Closed

    def _do_open(self, *args, **kwargs) -> None:
        # For override
        pass

    def _do_close(self, *args, **kwargs) -> None:
        # For override
        pass
