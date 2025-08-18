from typing import Any, Callable as _Callable, Optional, TYPE_CHECKING, Union

from ._stream import TradeDataStream
from ..._core.session import get_valid_session
from ..._tools import cached_property, create_repr
from ...delivery._stream import StreamOpenMixin

if TYPE_CHECKING:
    from ..._types import OptStrStrs, ExtendedParams, OptStr
    from ..._core.session import Session
    from ._stream import FinalizedOrders, UniverseTypes, Events


class Stream(StreamOpenMixin):
    def __init__(
        self,
        session: Optional["Session"] = None,
        universe: "OptStrStrs" = None,
        universe_type: Union[str, "UniverseTypes"] = None,
        fields: "OptStrStrs" = None,
        events: Union[str, "Events"] = None,
        finalized_orders: Union[str, "FinalizedOrders"] = None,
        filters: "OptStrStrs" = None,
        api: "OptStr" = None,
        extended_params: "ExtendedParams" = None,
    ):
        self._session = get_valid_session(session)
        self._always_use_default_session = session is None
        self._universe = universe
        self._fields = fields
        self._extended_params = extended_params
        self._universe_type = universe_type
        self._events = events
        self._finalized_orders = finalized_orders
        self._filters = filters
        self._api = api

    @cached_property
    def _stream(self):
        return TradeDataStream(
            session=self._session,
            universe=self._universe,
            fields=self._fields,
            extended_params=self._extended_params,
            universe_type=self._universe_type,
            events=self._events,
            finalized_orders=self._finalized_orders,
            filters=self._filters,
            api=self._api,
        )

    def on_update(self, on_update: _Callable[[dict, "Stream"], Any]) -> "Stream":
        """
        These notifications are emitted when fields of the requested instrument change

        Parameters
        ----------
        on_update : Callable
            Callable object to process retrieved data

        Returns
        -------
        current instance

        Examples
        -------
        >>> import datetime
        >>> from refinitiv.data.content import trade_data_service
        >>>
        >>> def display_event(event, stream):
        ...    current_time = datetime.datetime.now().time()
        ...    print("----------------------------------------------------------")
        ...    print(">>> {} event received at {}".format("Update", current_time))
        ...    print(event)
        >>>
        >>> definition = trade_data_service.Definition(
        ...     universe=[],
        ...     fields=[
        ...        "OrderKey",
        ...        "OrderTime",
        ...        "RIC",
        ...        "Side",
        ...        "AveragePrice",
        ...        "OrderStatus",
        ...        "OrderQuantity",
        ...],
        ...     events=trade_data_service.Events.Full,
        ...     finalized_orders=trade_data_service.FinalizedOrders.P1D
        ...)
        >>> stream = definition.get_stream()
        >>> stream.on_update(display_event)
        >>> stream.open()
        """
        self._stream.events.on_update(on_update)
        return self

    def on_complete(self, on_complete: _Callable[["Stream"], Any]) -> "Stream":
        """
        Full data of requested universe items

        Parameters
        ----------
        on_complete : Callable
            Callable object to process retrieved data

        Returns
        -------
        current instance

        Examples
        -------
        >>> import datetime
        >>> from refinitiv.data.content import trade_data_service
        >>>
        >>> def display_event(stream):
        ...    current_time = datetime.datetime.now().time()
        ...    print("----------------------------------------------------------")
        ...    print(">>> {} event received at {}".format("Complete", current_time))
        >>>
        >>> definition = trade_data_service.Definition(
        ...     universe=[],
        ...     fields=[
        ...        "OrderKey",
        ...        "OrderTime",
        ...        "RIC",
        ...        "Side",
        ...        "AveragePrice",
        ...        "OrderStatus",
        ...        "OrderQuantity",
        ...],
        ...     events=trade_data_service.Events.Full,
        ...     finalized_orders=trade_data_service.FinalizedOrders.P1D
        ...)
        >>> stream = definition.get_stream()
        >>> stream.on_complete(display_event)
        >>> stream.open()
        """
        self._stream.events.on_complete(on_complete)
        return self

    def on_add(self, on_add: _Callable[[dict, "Stream"], Any]) -> "Stream":
        """
        These notifications are sent when the status of one of the requested instruments
        is added

        Parameters
        ----------
        on_add : Callable
            Callable object to process retrieved data

        Returns
        -------
        current instance

        Examples
        -------
        >>> import datetime
        >>> from refinitiv.data.content import trade_data_service
        >>>
        >>> def display_event(event, stream):
        ...    current_time = datetime.datetime.now().time()
        ...    print("----------------------------------------------------------")
        ...    print(">>> {} event received at {}".format("Add", current_time))
        ...    print(event)
        >>>
        >>> definition = trade_data_service.Definition(
        ...     universe=[],
        ...     fields=[
        ...        "OrderKey",
        ...        "OrderTime",
        ...        "RIC",
        ...        "Side",
        ...        "AveragePrice",
        ...        "OrderStatus",
        ...        "OrderQuantity",
        ...],
        ...     events=trade_data_service.Events.Full,
        ...     finalized_orders=trade_data_service.FinalizedOrders.P1D
        ...)
        >>> stream = definition.get_stream()
        >>> stream.on_add(display_event)
        >>> stream.open()
        """
        self._stream.events.on_add(on_add)
        return self

    def on_remove(self, on_remove: _Callable[[dict, "Stream"], Any]) -> "Stream":
        """
        Called when the stream on summary order of universe is removed by the server.
        This callback is called with the reference to the stream object and
        the universe removed.

        Parameters
        ----------
        on_remove : Callable
            Callable object to process retrieved data

        Returns
        -------
        current instance

        Examples
        -------
        >>> import datetime
        >>> from refinitiv.data.content import trade_data_service
        >>>
        >>> def display_event(event, stream):
        ...    current_time = datetime.datetime.now().time()
        ...    print("----------------------------------------------------------")
        ...    print(">>> {} event received at {}".format("Remove", current_time))
        ...    print(event)
        >>>
        >>> definition = trade_data_service.Definition(
        ...     universe=[],
        ...     fields=[
        ...        "OrderKey",
        ...        "OrderTime",
        ...        "RIC",
        ...        "Side",
        ...        "AveragePrice",
        ...        "OrderStatus",
        ...        "OrderQuantity",
        ...],
        ...     events=trade_data_service.Events.Full,
        ...     finalized_orders=trade_data_service.FinalizedOrders.P1D
        ...)
        >>> stream = definition.get_stream()
        >>> stream.on_remove(display_event)
        >>> stream.open()
        """
        self._stream.events.on_remove(on_remove)
        return self

    def on_event(self, on_event: _Callable[[dict, "Stream"], Any]) -> "Stream":
        """
        These notifications are emitted when the status
        of one of the requested instruments changes

        Parameters
        ----------
        on_event

        Returns
        -------
        current instance

        Examples
        -------
        >>> import datetime
        >>> from refinitiv.data.content import trade_data_service
        >>>
        >>> def display_event(event, stream):
        ...    current_time = datetime.datetime.now().time()
        ...    print("----------------------------------------------------------")
        ...    print(">>> {} event received at {}".format("Event", current_time))
        ...    print(event)
        >>>
        >>> definition = trade_data_service.Definition(
        ...     universe=[],
        ...     fields=[
        ...        "OrderKey",
        ...        "OrderTime",
        ...        "RIC",
        ...        "Side",
        ...        "AveragePrice",
        ...        "OrderStatus",
        ...        "OrderQuantity",
        ...],
        ...     events=trade_data_service.Events.Full,
        ...     finalized_orders=trade_data_service.FinalizedOrders.P1D
        ...)
        >>> stream = definition.get_stream()
        >>> stream.on_event(display_event)
        >>> stream.open()
        """
        self._stream.events.on_event(on_event)
        return self

    def on_state(self, on_state: _Callable[[dict, "Stream"], Any]) -> "Stream":
        """
        These notifications are emitted when the state of one of the requested changes

        Parameters
        ----------
        on_state : Callable

        Returns
        -------
        current instance

        Examples
        -------
        >>> import datetime
        >>> from refinitiv.data.content import trade_data_service
        >>>
        >>> def display_event(event, stream):
        ...    current_time = datetime.datetime.now().time()
        ...    print("----------------------------------------------------------")
        ...    print(">>> {} event received at {}".format("State", current_time))
        ...    print(event)
        >>>
        >>> definition = trade_data_service.Definition(
        ...     universe=[],
        ...     fields=[
        ...        "OrderKey",
        ...        "OrderTime",
        ...        "RIC",
        ...        "Side",
        ...        "AveragePrice",
        ...        "OrderStatus",
        ...        "OrderQuantity",
        ...],
        ...     events=trade_data_service.Events.Full,
        ...     finalized_orders=trade_data_service.FinalizedOrders.P1D
        ...)
        >>> stream = definition.get_stream()
        >>> stream.on_state(display_event)
        >>> stream.open()
        """
        self._stream.events.on_state(on_state)
        return self

    def __repr__(self):
        return create_repr(self, class_name="Stream")
