from abc import abstractmethod
from typing import TYPE_CHECKING, Iterator

from ._basestream_states import BaseStreamState
from ._stream_states import (
    CloseStreamSt,
    OpeningStreamSt,
    OpenStreamSt,
    UnopenedStreamSt,
    StreamStates,
    StreamStateMixin,
)
from .._contrib_type import OptContribT
from ...._open_state import OpenState
from ...._tools import cached_property
from ...._types import OptDict

if TYPE_CHECKING:
    from .._contrib_response import ContribResponse


class OMMStreamStateMixin(StreamStateMixin):
    @abstractmethod
    def contribute(
        self, fields: dict, contrib_type: OptContribT = None, post_user_info: OptDict = None
    ) -> "ContribResponse":
        pass


class UnopenedOMMStreamSt(UnopenedStreamSt, OMMStreamStateMixin):
    def contribute(
        self, fields: dict, contrib_type: OptContribT = None, post_user_info: OptDict = None
    ) -> "ContribResponse":
        raise ValueError("Cannot contribute to an unopened stream")


class OpeningOMMStreamSt(OpeningStreamSt, OMMStreamStateMixin):
    def contribute(
        self, fields: dict, contrib_type: OptContribT = None, post_user_info: OptDict = None
    ) -> "ContribResponse":
        raise ValueError("Cannot contribute to an opening stream")


class OpenOMMStreamSt(OpenStreamSt, OMMStreamStateMixin):
    def contribute(
        self, fields: dict, contrib_type: OptContribT = None, post_user_info: OptDict = None
    ) -> "ContribResponse":
        return self.stream.do_contribute(fields, contrib_type, post_user_info)

    def can_transition_to(self, state: "BaseStreamState") -> bool:
        # open_st -> close_st
        # open_st -> contributing_st
        return state in {self.stream.states.close_st, self.stream.states.contributing_st}


class ContributingOMMStreamSt(BaseStreamState, OMMStreamStateMixin):
    def enter(self) -> None:
        self.stream.off_cxn_listeners(self.stream.cxn_listeners)
        self.stream.on_cxn_listeners(self.stream.contrib_listeners)

    def exit(self) -> None:
        self.stream.off_cxn_listeners(self.stream.contrib_listeners)
        self.stream.on_cxn_listeners(self.stream.cxn_listeners)

    def can_transition_to(self, state: "BaseStreamState") -> bool:
        # contributing_st -> open_st
        return state == self.stream.states.open_st

    def open(self, *args, **kwargs) -> OpenState:
        return OpenState.Opened

    def close(self, *args, **kwargs) -> OpenState:
        return OpenState.Opened

    def send(self, message: dict) -> bool:
        return self.stream.do_send(message)

    def contribute(
        self, fields: dict, contrib_type: OptContribT = None, post_user_info: OptDict = None
    ) -> "ContribResponse":
        raise ValueError(f"Cannot contribute to an already contributing stream")


class CloseOMMStreamSt(CloseStreamSt, OMMStreamStateMixin):
    def contribute(
        self, fields: dict, contrib_type: OptContribT = None, post_user_info: OptDict = None
    ) -> "ContribResponse":
        raise ValueError("Cannot contribute to a closed stream")


class OMMStreamStates(StreamStates):
    unopened_st_class = UnopenedOMMStreamSt
    opening_st_class = OpeningOMMStreamSt
    open_st_class = OpenOMMStreamSt
    close_st_class = CloseOMMStreamSt
    contributing_st_class = ContributingOMMStreamSt

    @cached_property
    def contributing_st(self):
        return self.contributing_st_class(self.stream)

    def __iter__(self) -> Iterator[BaseStreamState]:
        return iter(
            [
                self.unopened_st,
                self.opening_st,
                self.open_st,
                self.close_st,
                self.contributing_st,
            ]
        )
