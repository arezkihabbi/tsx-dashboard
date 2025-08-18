from functools import partialmethod

from ....delivery._stream import StreamEvt
from ....delivery._stream.events._stream_events import _RDPStreamEvts


def dispatch(self: _RDPStreamEvts, ev: StreamEvt, message: dict):
    self.dispatch(ev, self.originator.data, self.originator.column_names, self.originator)


class QuantitativeStreamEvts(_RDPStreamEvts):
    """
    Events from QuantitativeDataStream for User
    """

    dispatch_response = partialmethod(dispatch, StreamEvt.RESPONSE)
    dispatch_update = partialmethod(dispatch, StreamEvt.UPDATE)

    def dispatch_alarm(self, message: dict):
        self.dispatch(StreamEvt.ALARM, message.get("state"), self.originator)

    def dispatch_ack(self, message: dict):
        self.dispatch(StreamEvt.ACK, message.get("state"), self.originator)
