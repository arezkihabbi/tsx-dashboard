from typing import TYPE_CHECKING, Union

from ._stream import (
    Events,
    FinalizedOrders,
    UniverseTypes,
    universe_type_arg_parser,
    finalized_orders_arg_parser,
    events_arg_parser,
)
from ._stream_facade import Stream
from ..._tools import create_repr, try_copy_to_list

if TYPE_CHECKING:
    from ..._types import OptStr, ExtendedParams, OptStrStrs
    from ..._core.session import Session


class Definition:
    """
    This class describes Analytics Trade Data Service.

    Parameters
    ----------
    universe : list, optional
        A list of RIC or symbol or user's id for retrieving trading analytics data.
    fields : list, optional
        A list of enumerate fields.
    events : str or Events, optional
        Enable/Disable the detail of order event in the streaming.
        Default: False
    finalized_orders : str or FinalizedOrders, optional
        Enable/Disable the cached of finalized order of current day in the streaming.
        Default: False
    filters : list, optional
        Set the condition of subset of trading streaming data.
    universe_type : str or UniverseTypes, optional
        A type of given universe can be RIC, Symbol or UserID.
        Default: UniverseTypes.RIC
    api: str, optional
        Specifies the data source. It can be updated/added using config file
    extended_params : dict, optional
        If necessary other parameters

    Methods
    -------
    get_stream(session=session)
        Get stream object of this definition

    Examples
    --------
    >>> from refinitiv.data.content import trade_data_service
    >>> definition = trade_data_service.Definition()
    """

    def __init__(
        self,
        universe: "OptStrStrs" = None,
        universe_type: Union[str, UniverseTypes] = UniverseTypes.UserID,
        fields: "OptStrStrs" = None,
        events: Union[str, Events] = Events.No,
        finalized_orders: Union[str, FinalizedOrders] = FinalizedOrders.No,
        filters: "OptStrStrs" = None,
        api: "OptStr" = None,
        extended_params: "ExtendedParams" = None,
    ):
        self._universe = try_copy_to_list(universe)
        self._universe_type = universe_type_arg_parser.get_str(universe_type)
        self._fields = try_copy_to_list(fields)
        self._events = events_arg_parser.get_str(events)
        self._finalized_orders = finalized_orders_arg_parser.get_str(finalized_orders)
        self._filters = try_copy_to_list(filters)
        self._api = api
        self._extended_params = extended_params

    def __repr__(self):
        return create_repr(
            self,
            middle_path="content.trade_data_service",
            content={"universe": self._universe},
        )

    def get_stream(self, session: "Session" = None) -> Stream:
        """
        Returns a streaming trading analytics subscription.

        Parameters
        ----------
        session : Session, optional
            The Session used by the TradeDataService to retrieve data from the platform

        Returns
        -------
        TradeDataStream

        Examples
        --------
        >>> from refinitiv.data.content import trade_data_service
        >>> definition = trade_data_service.Definition()
        >>> stream = definition.get_stream()
        >>> stream.open()
        """
        stream = Stream(
            session=session,
            universe=self._universe,
            universe_type=self._universe_type,
            fields=self._fields,
            events=self._events,
            finalized_orders=self._finalized_orders,
            filters=self._filters,
            api=self._api,
            extended_params=self._extended_params,
        )
        return stream
