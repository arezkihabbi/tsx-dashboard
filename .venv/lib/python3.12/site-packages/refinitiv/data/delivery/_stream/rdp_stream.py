from typing import Any, Callable, TYPE_CHECKING, Optional

from ._basestream import StreamOpenMixin
from ._rdp_stream import _RDPStream
from .events import EventsType
from ..._core.session import get_valid_session
from ..._tools import cached_property, create_repr

if TYPE_CHECKING:
    from ..._types import ExtendedParams
    from ... import OpenState
    from ..._core.session import Session


class RDPStream(StreamOpenMixin):
    """
    Open an RDP stream.

    Parameters
    ----------

    service: string, optional
        name of RDP service

    universe: list
        RIC to retrieve item stream.

    view: list
        data fields to retrieve item stream

    parameters: dict
        extra parameters to retrieve item stream.

    api: string
        specific name of RDP streaming defined in config file. i.e.
        'streaming/trading-analytics/redi'

    extended_params: dict, optional
        Specify optional params
        Default: None

    Raises
    ------
    Exception
        If request fails or if Refinitiv Services return an error

    Examples
    --------
    >>> import refinitiv.data as rd
    >>> APP_KEY = "APP_KEY"
    >>> USERNAME = "USERNAME"
    >>> PASSWORD = "PASSWORD"
    >>> session = rd.session.platform.Definition(
    ...         app_key=APP_KEY,
    ...         grant=rd.session.platform.GrantPassword(
    ...             username=USERNAME,
    ...             password=PASSWORD,
    ...         )
    ... ).get_session()
    >>> session.open()
    >>>
    >>> tds = rd.delivery.rdp_stream.Definition(
    ...     service="",
    ...     universe=[],
    ...     view=[],
    ...     parameters={"universeType": "RIC"},
    ...     api='streaming.trading-analytics.endpoints.redi'
    ... ).get_stream(session)
    >>> tds.open()
    """

    def __init__(
        self,
        service: str,
        universe: list,
        view: list,
        parameters: dict,
        api: str,
        session: Optional["Session"] = None,
        extended_params: "ExtendedParams" = None,
    ) -> None:
        self._session = get_valid_session(session)
        self._always_use_default_session = session is None
        self._service = service
        self._universe = universe
        self._view = view
        self._parameters = parameters
        self._api = api
        self._extended_params = extended_params

    @cached_property
    def _stream(self) -> _RDPStream:
        return _RDPStream(
            session=self._session,
            universe=self._universe,
            view=self._view,
            service=self._service,
            api=self._api,
            parameters=self._parameters,
            extended_params=self._extended_params,
            events_type=EventsType.RDP_MESSAGE_ORIGINATOR,
        )

    def open(self) -> "OpenState":
        """
        Opens the RDPStream to start to stream. Once it's opened,
        it can be used in order to retrieve data.

        Parameters
        ----------

        Returns
        -------
        OpenState
            current state of this RDP stream object.

        Examples
        --------
        >>> from refinitiv.data.delivery import rdp_stream
        >>> import asyncio
        >>> definition = rdp_stream.Definition(
        ...                    service=None,
        ...                    universe=[],
        ...                    view=None,
        ...                    parameters={"universeType": "RIC"},
        ...                    api='streaming.trading-analytics.endpoints.redi')
        >>> stream = definition.get_stream()
        >>> asyncio.run(stream.open_async())
        """
        return super().open()

    async def open_async(self) -> "OpenState":
        """
        Opens asynchronously the RDPStream to start to stream

        Parameters
        ----------

        Returns
        -------
        OpenState
            current state of this RDP stream object.

        Examples
        --------
        >>> from refinitiv.data.delivery import rdp_stream
        >>> import asyncio
        >>> definition = rdp_stream.Definition(
        ...                     service=None,
        ...                     universe=[],
        ...                     view=None,
        ...                     parameters={"universeType": "RIC"},
        ...                     api='streaming.trading-analytics.endpoints.redi')
        >>> stream = definition.get_stream()
        >>> asyncio.run(stream.open_async())
        """
        return await super().open_async()

    def close(self) -> "OpenState":
        """
        Closes the RPDStream connection, releases resources

        Returns
        -------
        OpenState
            current state of this RDP stream object.

        Examples
        --------
        >>> from refinitiv.data.delivery import rdp_stream
        >>> definition = rdp_stream.Definition(
        ...                    service=None,
        ...                    universe=[],
        ...                    view=None,
        ...                    parameters={"universeType": "RIC"},
        ...                    api='streaming.trading-analytics.endpoints.redi')
        >>> stream = definition.get_stream()
        >>> stream.open()
        >>> stream.close()
        """
        return super().close()

    def on_ack(self, on_ack: Callable[[dict, "RDPStream"], Any]) -> "RDPStream":
        """
        This function called when the stream received an ack message.

        Parameters
        ----------
        on_ack : Callable, optional
             Callable object to process retrieved ack data

        Returns
        -------
        RDPStream
            current instance it is a RDP stream object.

        Examples
        --------
        Prerequisite: The default session must be opened.
        >>> from datetime import datetime
        >>> from refinitiv.data.delivery import rdp_stream
        >>>
        >>> def display_response(event, stream):
        ...     print(f'Ack received at {datetime.now}')
        ...     print(event)
        >>>
        >>> definition = rdp_stream.Definition(
        ...                     service=None,
        ...                     universe=[],
        ...                     view=None,
        ...                     parameters={"universeType": "RIC"},
        ...                     api='streaming.trading-analytics.endpoints.redi')
        >>> stream = definition.get_stream()
        >>> stream.on_ack(display_response)
        >>>
        >>> stream.open()
        """
        self._stream.on_ack(on_ack)
        return self

    def on_response(self, on_response: Callable[[dict, "RDPStream"], Any]) -> "RDPStream":
        """
        This function called when the stream received an response message.

        Parameters
        ----------
        on_response : Callable, optional
             Callable object to process retrieved response data

        Returns
        -------
        RDPStream
            current instance it is a RDP stream object.

        Examples
        --------
        Prerequisite: The default session must be opened.
        >>> from datetime import datetime
        >>> from refinitiv.data.delivery import rdp_stream
        >>>
        >>> def display_response(event, stream):
        ...     print(f'Response received at {datetime.now}')
        ...     print(event)
        >>>
        >>> definition = rdp_stream.Definition(
        ...                    service=None,
        ...                    universe=[],
        ...                    view=None,
        ...                    parameters={"universeType": "RIC"},
        ...                    api='streaming.trading-analytics.endpoints.redi')
        >>> stream = definition.get_stream()
        >>> stream.on_response(display_response)
        >>>
        >>> stream.open()
        """
        self._stream.on_response(on_response)
        return self

    def on_update(self, on_update: Callable[[dict, "RDPStream"], Any]) -> "RDPStream":
        """
        This function called when the stream received an update message.

        Parameters
        ----------
        on_update : Callable, optional
             Callable object to process retrieved update data

        Returns
        -------
        RDPStream
            current instance it is a RDP stream object.

        Examples
        --------
        Prerequisite: The default session must be opened.
        >>> from datetime import datetime
        >>> from refinitiv.data.delivery import rdp_stream
        >>>
        >>> def display_response(event, stream):
        ...     print(f'Update received at {datetime.now}')
        ...     print(event)
        >>>
        >>> definition = rdp_stream.Definition(
        ...                    service=None,
        ...                    universe=[],
        ...                    view=None,
        ...                    parameters={"universeType": "RIC"},
        ...                    api='streaming.trading-analytics.endpoints.redi')
        >>> stream = definition.get_stream()
        >>> stream.on_update(display_response)
        >>>
        >>> stream.open()
        """
        self._stream.on_update(on_update)
        return self

    def on_alarm(self, on_alarm: Callable[[dict, "RDPStream"], Any]) -> "RDPStream":
        """
        This function called when the stream received an alarm message.

        Parameters
        ----------
        on_alarm : Callable, optional
             Callable object to process retrieved alarm data

        Returns
        -------
        RDPStream
            current instance it is a RDP stream object.

        Examples
        --------
        Prerequisite: The default session must be opened.
        >>> from datetime import datetime
        >>> from refinitiv.data.delivery import rdp_stream
        >>>
        >>> def display_response(event, stream):
        ...     print(f'Alarm received at {datetime.now}')
        ...     print(event)
        >>>
        >>> definition = rdp_stream.Definition(
        ...                    service=None,
        ...                    universe=[],
        ...                    view=None,
        ...                    parameters={"universeType": "RIC"},
        ...                    api='streaming.trading-analytics.endpoints.redi')
        >>> stream = definition.get_stream()
        >>> stream.on_alarm(display_response)
        >>>
        >>> stream.open()
        """
        self._stream.on_alarm(on_alarm)
        return self

    def __repr__(self):
        return create_repr(self, middle_path="rdp_stream", class_name=self.__class__.__name__)
