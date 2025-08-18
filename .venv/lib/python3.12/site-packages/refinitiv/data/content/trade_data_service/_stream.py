import re
from typing import TYPE_CHECKING, Union

from ._events import TradeDataStreamEvts
from ._listeners import TDSStreamListeners
from ..._base_enum import StrEnum
from ..._content_type import ContentType
from ..._tools import make_enum_arg_parser, cached_property
from ..._types import ExtendedParams, Strings, OptStr, OptStrStrs
from ...delivery._stream import _RDPStream

if TYPE_CHECKING:
    from ..._core.session import Session

QUEUE_SIZE_PATTERN = re.compile(r"^queueSize=(?P<queue_size>[0-9]+)")


class Events(StrEnum):
    """Events"""

    No = "None"
    Full = "Full"


class FinalizedOrders(StrEnum):
    """Finalized order in cached"""

    No = "None"
    P1D = "P1D"


class UniverseTypes(StrEnum):
    """Universe Types"""

    RIC = "RIC"
    Symbol = "Symbol"
    UserID = "UserID"


universe_type_arg_parser = make_enum_arg_parser(UniverseTypes, can_be_lower=True)
finalized_orders_arg_parser = make_enum_arg_parser(FinalizedOrders, can_be_lower=True)
events_arg_parser = make_enum_arg_parser(Events, can_be_lower=True)


class TradeDataStream(_RDPStream):
    """
    Open a streaming trading analytics subscription.

    Parameters
    ----------
    universe: list
        a list of RIC or symbol or user's id for retrieving trading analytics data.

    fields: list
        a list of enumerate fields.
        Default: None

    universe_type: enum
        a type of given universe can be RIC, Symbol or UserID.
        Default: UniverseTypes.RIC

    finalized_orders: bool
        enable/disable the cached of finalized order of current day in the streaming.
        Default: False

    filters: list
        set the condition of subset of trading streaming data
        Default: None

    """

    def __init__(
        self,
        session: "Session",
        universe: OptStrStrs = None,
        universe_type: Union[str, UniverseTypes] = None,
        fields: OptStrStrs = None,
        events: Union[str, "Events"] = None,
        finalized_orders: Union[str, "FinalizedOrders"] = None,
        filters: OptStrStrs = None,
        api: OptStr = None,
        extended_params: ExtendedParams = None,
    ):
        parameters = {
            "universeType": universe_type,
            "events": events,
            "finalizedOrders": finalized_orders,
        }
        if filters is not None:
            parameters["filters"] = filters

        view = None
        if fields:
            view = fields.copy()

        _RDPStream.__init__(
            self,
            session=session,
            universe=universe,
            view=view,
            api=api,
            parameters=parameters,
            extended_params=extended_params,
            content_type=ContentType.STREAMING_TRADING,
        )
        self.headers_ids: "Strings" = []
        self.is_completed: bool = False

    @cached_property
    def events(self) -> TradeDataStreamEvts:
        return TradeDataStreamEvts(self)

    @cached_property
    def cxn_listeners(self) -> TDSStreamListeners:
        return TDSStreamListeners(self)

    def process_data(self, message: dict) -> None:
        data = message.get("data", [])
        for datum in data:
            self.events.dispatch_add(dict(zip(self.headers_ids, datum)))

    def process_state(self, message: dict) -> None:
        state = message.get("state", {})

        if "message" in state:
            matched = QUEUE_SIZE_PATTERN.match(state["message"])

            if matched is not None:
                group = matched.groupdict()
                queue_size = group.get("queue_size", -1)
                queue_size = int(queue_size)

                if queue_size == 0 and not self.is_completed:
                    self.is_completed = True
                    self.events.dispatch_complete()

        if state:
            self.events.dispatch_state(state)
