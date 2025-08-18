from functools import partialmethod
from typing import TYPE_CHECKING

from ..delivery._stream import StreamEvt
from ..delivery._stream.events import _OMMStreamEvts

if TYPE_CHECKING:
    from ._universe_stream import _UniverseStream
    from ._universe_streams import _UniverseStreams  # noqa: F401


def dispatch(self: _OMMStreamEvts, ev: StreamEvt, message: dict, universe_stream: "_UniverseStream"):
    self.dispatch(ev, message, universe_stream.name, self.originator)


class _UniverseStreamsEvts(_OMMStreamEvts):
    """
    Events from _UniverseStreams for User
    """

    dispatch_refresh = partialmethod(dispatch, StreamEvt.REFRESH)
    dispatch_status = partialmethod(dispatch, StreamEvt.STATUS)
    dispatch_complete = partialmethod(_OMMStreamEvts._dispatch_org, StreamEvt.COMPLETE)
    dispatch_error = partialmethod(dispatch, StreamEvt.ERROR)
    dispatch_update = partialmethod(dispatch, StreamEvt.UPDATE)
    dispatch_ack = partialmethod(dispatch, StreamEvt.ACK)
