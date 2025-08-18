from enum import Enum, auto
from typing import Any, Dict, Type, TYPE_CHECKING

from ._stream_events import OMMStreamEvts, _OMMStreamEvts, _RDPStreamEvts, RDPStreamEvts, OMMStreamEvtsMsgOrg

if TYPE_CHECKING:
    from ._stream_events import MessageStreamEvts
    from .._stream import Stream


class EventsType(Enum):
    OMM_ORIGINATOR_MESSAGE = auto()
    OMM_MESSAGE_OWNER = auto()
    OMM_MESSAGE_ORIGINATOR = auto()
    RDP_MESSAGE_ORIGINATOR = auto()
    RDP_ORIGINATOR_MESSAGE = auto()


events_class_by_events_type: Dict[EventsType, Type["MessageStreamEvts"]] = {
    EventsType.OMM_ORIGINATOR_MESSAGE: _OMMStreamEvts,
    EventsType.OMM_MESSAGE_ORIGINATOR: OMMStreamEvtsMsgOrg,
    EventsType.OMM_MESSAGE_OWNER: OMMStreamEvts,
    EventsType.RDP_MESSAGE_ORIGINATOR: RDPStreamEvts,
    EventsType.RDP_ORIGINATOR_MESSAGE: _RDPStreamEvts,
}


def create_events(events_type: EventsType, originator: "Stream", owner: Any = None) -> "MessageStreamEvts":
    events_class = events_class_by_events_type.get(events_type)

    if events_class is None:
        raise ValueError(f"Unknown events type {events_type}")

    if events_type is EventsType.OMM_MESSAGE_OWNER and not owner:
        raise ValueError("Owner must be provided for EventsType.OMM_MESSAGE_OWNER")

    return events_class(originator)
