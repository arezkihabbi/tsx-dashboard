from functools import partialmethod
from typing import TYPE_CHECKING

from ._events import Events_SimpleDict
from ..event import StreamEvt, CxnEvent, StreamStEvt
from ...._listener import OriginatorType

if TYPE_CHECKING:
    from .. import _RDPStream, _OMMStream  # noqa: F401


class BaseStreamEvts(Events_SimpleDict[OriginatorType]):
    """
    Events from BaseStream for User
    """

    on_close = partialmethod(Events_SimpleDict.on, StreamStEvt.CLOSE)
    on_open = partialmethod(Events_SimpleDict.on, StreamStEvt.OPEN)
    off_close = partialmethod(Events_SimpleDict.off, StreamStEvt.CLOSE)
    off_open = partialmethod(Events_SimpleDict.off, StreamStEvt.OPEN)
    dispatch_open = partialmethod(Events_SimpleDict.dispatch, StreamStEvt.OPEN)
    dispatch_close = partialmethod(Events_SimpleDict.dispatch, StreamStEvt.CLOSE)


class StreamEvts(BaseStreamEvts[OriginatorType]):
    """
    Events from Stream for User
    """

    on_disconnecting = partialmethod(BaseStreamEvts.on, CxnEvent.DISCONNECTING)
    on_reconnected = partialmethod(BaseStreamEvts.on, CxnEvent.RECONNECTED)
    on_disposed = partialmethod(BaseStreamEvts.on, CxnEvent.DISPOSED)
    off_disconnecting = partialmethod(BaseStreamEvts.off, CxnEvent.DISCONNECTING)
    off_reconnected = partialmethod(BaseStreamEvts.off, CxnEvent.RECONNECTED)
    off_disposed = partialmethod(BaseStreamEvts.off, CxnEvent.DISPOSED)
    dispatch_disconnecting = partialmethod(BaseStreamEvts.dispatch, CxnEvent.DISCONNECTING)
    dispatch_reconnected = partialmethod(BaseStreamEvts.dispatch, CxnEvent.RECONNECTED)
    dispatch_disposed = partialmethod(BaseStreamEvts.dispatch, CxnEvent.DISPOSED)

    def _dispatch_org_msg(self, ev: StreamEvt, message: dict):
        self.dispatch(ev, self.originator, message)

    def _dispatch_msg_org(self, ev: StreamEvt, message: dict):
        self.dispatch(ev, message, self.originator)

    def _dispatch_msg_owner(self, ev: StreamEvt, message: dict):
        self.dispatch(ev, message, self.originator.owner)

    def _dispatch_org(self, ev: StreamEvt, message: dict):
        self.dispatch(ev, self.originator)


class MessageStreamEvts(StreamEvts[OriginatorType]):
    """
    Events from MessageStream for User
    """

    on_ack = partialmethod(StreamEvts.on, StreamEvt.ACK)
    on_update = partialmethod(StreamEvts.on, StreamEvt.UPDATE)
    off_ack = partialmethod(StreamEvts.off, StreamEvt.ACK)
    off_update = partialmethod(StreamEvts.off, StreamEvt.UPDATE)
    dispatch_ack = partialmethod(StreamEvts._dispatch_org_msg, StreamEvt.ACK)
    dispatch_update = partialmethod(StreamEvts._dispatch_org_msg, StreamEvt.UPDATE)


class _OMMStreamEvts(MessageStreamEvts["_OMMStream"]):
    """
    Events from _OMMStream for User
    """

    on_refresh = partialmethod(MessageStreamEvts.on, StreamEvt.REFRESH)
    on_status = partialmethod(MessageStreamEvts.on, StreamEvt.STATUS)
    on_complete = partialmethod(MessageStreamEvts.on, StreamEvt.COMPLETE)
    on_error = partialmethod(MessageStreamEvts.on, StreamEvt.ERROR)
    off_refresh = partialmethod(MessageStreamEvts.off, StreamEvt.REFRESH)
    off_status = partialmethod(MessageStreamEvts.off, StreamEvt.STATUS)
    off_complete = partialmethod(MessageStreamEvts.off, StreamEvt.COMPLETE)
    off_error = partialmethod(MessageStreamEvts.off, StreamEvt.ERROR)
    dispatch_refresh = partialmethod(MessageStreamEvts._dispatch_org_msg, StreamEvt.REFRESH)
    dispatch_status = partialmethod(MessageStreamEvts._dispatch_org_msg, StreamEvt.STATUS)
    dispatch_complete = partialmethod(MessageStreamEvts._dispatch_org_msg, StreamEvt.COMPLETE)
    dispatch_error = partialmethod(MessageStreamEvts._dispatch_org_msg, StreamEvt.ERROR)


class OMMStreamEvtsMsgOrg(_OMMStreamEvts):
    """
    Events from _OMMStream for User
    """

    dispatch_refresh = partialmethod(MessageStreamEvts._dispatch_msg_org, StreamEvt.REFRESH)
    dispatch_status = partialmethod(MessageStreamEvts._dispatch_msg_org, StreamEvt.STATUS)
    dispatch_complete = partialmethod(MessageStreamEvts._dispatch_msg_org, StreamEvt.COMPLETE)
    dispatch_error = partialmethod(MessageStreamEvts._dispatch_msg_org, StreamEvt.ERROR)
    dispatch_update = partialmethod(MessageStreamEvts._dispatch_msg_org, StreamEvt.UPDATE)
    dispatch_ack = partialmethod(MessageStreamEvts._dispatch_msg_org, StreamEvt.ACK)


class OMMStreamEvts(_OMMStreamEvts):
    """
    Events from OMMStream for User
    """

    dispatch_refresh = partialmethod(MessageStreamEvts._dispatch_msg_owner, StreamEvt.REFRESH)
    dispatch_status = partialmethod(MessageStreamEvts._dispatch_msg_owner, StreamEvt.STATUS)
    dispatch_complete = partialmethod(MessageStreamEvts._dispatch_msg_owner, StreamEvt.COMPLETE)
    dispatch_error = partialmethod(MessageStreamEvts._dispatch_msg_owner, StreamEvt.ERROR)
    dispatch_update = partialmethod(MessageStreamEvts._dispatch_msg_owner, StreamEvt.UPDATE)
    dispatch_ack = partialmethod(MessageStreamEvts._dispatch_msg_owner, StreamEvt.ACK)


class _RDPStreamEvts(MessageStreamEvts["_RDPStream"]):
    """
    Events from _RDPStream for User
    """

    on_alarm = partialmethod(MessageStreamEvts.on, StreamEvt.ALARM)
    on_response = partialmethod(MessageStreamEvts.on, StreamEvt.RESPONSE)
    off_alarm = partialmethod(MessageStreamEvts.off, StreamEvt.ALARM)
    off_response = partialmethod(MessageStreamEvts.off, StreamEvt.RESPONSE)
    dispatch_alarm = partialmethod(MessageStreamEvts._dispatch_org_msg, StreamEvt.ALARM)
    dispatch_response = partialmethod(MessageStreamEvts._dispatch_org_msg, StreamEvt.RESPONSE)


class RDPStreamEvts(_RDPStreamEvts):
    """
    Events from RDPStream for User
    """

    dispatch_alarm = partialmethod(MessageStreamEvts._dispatch_msg_org, StreamEvt.ALARM)
    dispatch_response = partialmethod(MessageStreamEvts._dispatch_msg_org, StreamEvt.RESPONSE)
    dispatch_update = partialmethod(MessageStreamEvts._dispatch_msg_org, StreamEvt.UPDATE)
    dispatch_ack = partialmethod(MessageStreamEvts._dispatch_msg_org, StreamEvt.ACK)
