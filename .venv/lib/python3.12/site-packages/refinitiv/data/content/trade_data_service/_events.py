from functools import partialmethod

from ..._base_enum import StrEnum
from ...delivery._stream.events import RDPStreamEvts


class TradeDataStreamEvent(StrEnum):
    ADD = "add"
    COMPLETE = "complete"
    EVENT = "event"
    REMOVE = "remove"
    STATE = "state"


class TradeDataStreamEvts(RDPStreamEvts):
    """
    Events for TradeDataStream.
    """

    on_add = partialmethod(RDPStreamEvts.on, TradeDataStreamEvent.ADD)
    on_complete = partialmethod(RDPStreamEvts.on, TradeDataStreamEvent.COMPLETE)
    on_event = partialmethod(RDPStreamEvts.on, TradeDataStreamEvent.EVENT)
    on_remove = partialmethod(RDPStreamEvts.on, TradeDataStreamEvent.REMOVE)
    on_state = partialmethod(RDPStreamEvts.on, TradeDataStreamEvent.STATE)
    dispatch_add = partialmethod(RDPStreamEvts.dispatch, TradeDataStreamEvent.ADD)
    dispatch_complete = partialmethod(RDPStreamEvts.dispatch, TradeDataStreamEvent.COMPLETE)
    dispatch_event = partialmethod(RDPStreamEvts.dispatch, TradeDataStreamEvent.EVENT)
    dispatch_remove = partialmethod(RDPStreamEvts.dispatch, TradeDataStreamEvent.REMOVE)
    dispatch_state = partialmethod(RDPStreamEvts.dispatch, TradeDataStreamEvent.STATE)
