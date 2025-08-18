from functools import partialmethod
from typing import List

from ...._base_enum import StrEnum
from ....delivery._stream import StreamEvt
from ....delivery._stream.events import OMMStreamEvts


class StreamingChainEvent(StrEnum):
    ADD = "streaming_chain_add_event"
    REMOVE = "streaming_chain_remove_event"


def dispatch(self: OMMStreamEvts, ev: StreamingChainEvent, constituent: str, index: int):
    self.dispatch(ev, constituent, index, self.originator)


class StreamingChainEvts(OMMStreamEvts):
    """
    Events from StreamingChain for User
    """

    on_add = partialmethod(OMMStreamEvts.on, StreamingChainEvent.ADD)
    on_remove = partialmethod(OMMStreamEvts.on, StreamingChainEvent.REMOVE)
    off_add = partialmethod(OMMStreamEvts.off, StreamingChainEvent.ADD)
    off_remove = partialmethod(OMMStreamEvts.off, StreamingChainEvent.REMOVE)
    dispatch_add = partialmethod(dispatch, StreamingChainEvent.ADD)
    dispatch_remove = partialmethod(dispatch, StreamingChainEvent.REMOVE)

    def dispatch_update(self, new_constituent: str, old_constituent: str, index: int):
        self.dispatch(StreamEvt.UPDATE, new_constituent, old_constituent, index, self.originator)

    def dispatch_complete(self, constituents: List[str]):
        self.dispatch(StreamEvt.COMPLETE, constituents, self.originator)

    def dispatch_error(self, message: dict, name: str):
        self.dispatch(StreamEvt.ERROR, (message,), name, self.originator)
