from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, TypeVar, Generic, Type, Iterator

from ...._open_state import OpenState
from ...._tools import cached_property

if TYPE_CHECKING:
    from .._basestream import BaseStream

StreamType = TypeVar("StreamType", bound="BaseStream")


class BaseStreamState(Generic[StreamType], ABC):
    def __init__(self, stream: StreamType):
        super().__init__()
        self.stream: StreamType = stream

    def enter(self) -> None:
        pass

    def exit(self) -> None:
        pass

    @abstractmethod
    def can_transition_to(self, state: "BaseStreamState") -> bool:
        pass

    @abstractmethod
    def open(self, *args, **kwargs) -> OpenState:
        pass

    @abstractmethod
    def close(self, *args, **kwargs) -> OpenState:
        pass

    def __repr__(self) -> str:
        return self.__class__.__name__

    def __str__(self):
        return repr(self)


class UnopenedBaseStreamSt(BaseStreamState[StreamType]):
    open_state: OpenState = OpenState.Closed

    def can_transition_to(self, state: "BaseStreamState") -> bool:
        # unopened_st -> opening_st
        return state == self.stream.states.opening_st

    def open(self, *args, **kwargs) -> OpenState:
        return self.stream.do_open(*args, **kwargs)

    def close(self, *args, **kwargs) -> OpenState:
        return self.open_state


class OpeningBaseStreamSt(BaseStreamState):
    open_state: OpenState = OpenState.Pending

    def can_transition_to(self, state: "BaseStreamState") -> bool:
        # opening_st -> open_st
        # opening_st -> close_st
        return state in {self.stream.states.open_st, self.stream.states.close_st}

    def open(self, *args, **kwargs) -> OpenState:
        return self.open_state

    def close(self, *args, **kwargs) -> OpenState:
        return self.stream.do_close(*args, **kwargs)


class OpenBaseStreamSt(BaseStreamState):
    open_state: OpenState = OpenState.Opened

    def can_transition_to(self, state: "BaseStreamState") -> bool:
        # open_st -> close_st
        return state == self.stream.states.close_st

    def open(self, *args, **kwargs) -> OpenState:
        return self.open_state

    def close(self, *args, **kwargs) -> OpenState:
        return self.stream.do_close(*args, **kwargs)


class CloseBaseStreamSt(BaseStreamState):
    open_state: OpenState = OpenState.Closed

    def can_transition_to(self, state: "BaseStreamState") -> bool:
        # close_st -> opening_st
        return state == self.stream.states.opening_st

    def close(self, *args, **kwargs) -> OpenState:
        return self.open_state

    def open(self, *args, **kwargs) -> OpenState:
        return self.stream.do_open(*args, **kwargs)


class BaseStreamStates:
    unopened_st_class: Type[BaseStreamState] = UnopenedBaseStreamSt
    opening_st_class: Type[BaseStreamState] = OpeningBaseStreamSt
    open_st_class: Type[BaseStreamState] = OpenBaseStreamSt
    close_st_class: Type[BaseStreamState] = CloseBaseStreamSt

    def __init__(
        self,
        stream: "BaseStream",
    ) -> None:
        super().__init__()
        self.stream = stream

    @cached_property
    def unopened_st(self):
        return self.unopened_st_class(self.stream)

    @cached_property
    def opening_st(self):
        return self.opening_st_class(self.stream)

    @cached_property
    def open_st(self):
        return self.open_st_class(self.stream)

    @cached_property
    def close_st(self):
        return self.close_st_class(self.stream)

    def __iter__(self) -> Iterator[BaseStreamState]:
        return iter([self.unopened_st, self.opening_st, self.open_st, self.close_st])
