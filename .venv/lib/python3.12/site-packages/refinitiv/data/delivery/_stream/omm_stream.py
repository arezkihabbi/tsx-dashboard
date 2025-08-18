from typing import Any, Callable, Optional, TYPE_CHECKING

from ._basestream import StreamOpenWithUpdatesMixin
from ._omm_stream import _OMMStream
from ._stream_factory import get_service_and_details_omm
from .events import EventsType
from ..._content_type import ContentType
from ..._core.session import get_valid_session
from ..._tools import cached_property, create_repr

if TYPE_CHECKING:
    from ... import OpenState
    from ..._core.session import Session
    from ._contrib_response import ContribResponse
    from ._contrib_type import OptContribT
    from ..._types import ExtendedParams, OptStr, Strings, OptDict


class OMMStream(StreamOpenWithUpdatesMixin):
    """
    Open an OMM stream.

    Parameters
    ----------
    session: Session
        The Session defines the source where you want to retrieve your data

    name: string
        RIC to retrieve item stream.

    api: string, optional
        specific name of RDP streaming defined in config file.
        i.e. 'streaming.trading-analytics.endpoints.redi'
        Default: 'streaming.trading-analytics.endpoints.redi'

    domain: string
        Specify item stream domain (MarketPrice, MarketByPrice, ...)
        Default : "MarketPrice"

    service: string, optional
        Specify the service to subscribe on.
        Default: None

    fields: string or list, optional
        Specify the fields to retrieve.
        Default: None

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
    >>> APP_KEY = "app_key"
    >>> session = rd.session.desktop.Definition(app_key=APP_KEY).get_session()
    >>> session.open()
    >>>
    >>> euro = rd.delivery.omm_stream.Definition("EUR=").get_stream(session)
    >>> euro.open()
    >>>
    >>> def on_update_callback(stream, msg):
    ...     print(msg)
    >>>
    >>> definition = rd.delivery.omm_stream.Definition("THB=")
    >>> thb = definition.get_stream(session)
    >>> thb.on_update(on_update_callback)
    >>> thb.open()
    """

    def __init__(
        self,
        name: str,
        session: Optional["Session"] = None,
        api: "OptStr" = None,
        domain: str = "MarketPrice",
        service: "OptStr" = None,
        fields: Optional["Strings"] = None,
        extended_params: "ExtendedParams" = None,
    ) -> None:
        self._session = get_valid_session(session)
        self._always_use_default_session = session is None
        self._name = name
        self._api = api
        self._domain = domain
        self._service = service
        self._fields = fields
        self._extended_params = extended_params

    @cached_property
    def _stream(self) -> _OMMStream:
        session = self._session
        service, details = get_service_and_details_omm(ContentType.STREAMING_OMM, session, self._service, self._api)
        return _OMMStream(
            stream_id=session._get_omm_stream_id(),
            session=session,
            name=self._name,
            domain=self._domain,
            service=service,
            fields=self._fields,
            details=details,
            extended_params=self._extended_params,
            owner=self,
            events_type=EventsType.OMM_MESSAGE_ORIGINATOR,
        )

    @property
    def status(self) -> dict:
        return {
            "status": self._stream.state,
            "code": self._stream.status_stream_state,
            "message": self._stream.status_message_state,
        }

    def open(self, with_updates: bool = True) -> "OpenState":
        """
        Opens the OMMStream to start to stream.
        Once it's opened, it can be used in order to retrieve data.

        Parameters
        ----------
        with_updates : bool, optional
            actions:
                True - the streaming will work as usual
                        and the data will be received continuously.
                False - only one data snapshot will be received
                        (single Refresh 'NonStreaming') and
                        stream will be closed automatically.

            Defaults to True

        Returns
        -------
        OpenState
            current state of this OMM stream object.

        Examples
        --------
        >>> from refinitiv.data.delivery import omm_stream
        >>> definition = omm_stream.Definition("EUR")
        >>> stream = definition.get_stream()
        >>> stream.open()
        """
        return super().open(with_updates=with_updates)

    async def open_async(self, with_updates: bool = True) -> "OpenState":
        """
        Opens asynchronously the OMMStream to start to stream

        Parameters
        ----------
        with_updates : bool, optional
            actions:
                True - the streaming will work as usual
                        and the data will be received continuously.
                False - only one data snapshot will be received
                        (single Refresh 'NonStreaming') and
                        stream will be closed automatically.

        Returns
        -------
        OpenState
            current state of this OMM stream object.

        Examples
        --------
        >>> from refinitiv.data.delivery import omm_stream
        >>> import asyncio
        >>> definition = omm_stream.Definition("EUR")
        >>> stream = definition.get_stream()
        >>> asyncio.run(stream.open_async())
        """
        return await super().open_async(with_updates=with_updates)

    def close(self) -> "OpenState":
        """
        Closes the OMMStream connection, releases resources

        Returns
        -------
        OpenState
            current state of this OMM stream object.

        Examples
        --------
        >>> from refinitiv.data.delivery import omm_stream
        >>> definition = omm_stream.Definition("EUR")
        >>> stream = definition.get_stream()
        >>> stream.open()
        >>> stream.close()
        """
        return super().close()

    def on_refresh(self, func: Callable[[dict, "OMMStream"], Any]) -> "OMMStream":
        """
        This function called when the stream is opened or
        when the record is refreshed with a new image.
        This callback receives a full image.

        Parameters
        ----------
        func : Callable, optional
             Callable object to process retrieved refresh data

        Returns
        -------
        OMMStream
            current instance is an OMM stream object.

        Examples
        --------
        Prerequisite: The default session must be opened.
        >>> from datetime import datetime
        >>> from refinitiv.data.delivery import omm_stream
        >>>
        >>> def display_response(event, stream):
        ...      print(f'Refresh received at {datetime.now}')
        ...      print(event)
        >>>
        >>> definition = omm_stream.Definition("EUR")
        >>> stream = definition.get_stream()
        >>> stream.on_refresh(display_response)
        >>>
        >>> stream.open()
        """
        self._stream.on_refresh(func)
        return self

    def on_update(self, func: Callable[[dict, "OMMStream"], Any]) -> "OMMStream":
        """
        This function called when an update is received.

        Parameters
        ----------
        func : Callable, optional
            Callable object to process retrieved update data

        Returns
        -------
        OMMStream
            current instance is an OMM stream object.

        Examples
        --------
        Prerequisite: The default session must be opened.
        >>> from datetime import datetime
        >>> from refinitiv.data.delivery import omm_stream
        >>>
        >>> def display_response(event, stream):
        ...     print(f'Update received at {datetime.now}')
        ...     print(event)
        >>>
        >>> definition = omm_stream.Definition("EUR")
        >>> stream = definition.get_stream()
        >>> stream.on_update(display_response)
        >>>
        >>> stream.open()
        """
        self._stream.on_update(func)
        return self

    def on_status(self, func: Callable[[dict, "OMMStream"], Any]) -> "OMMStream":
        """
        This function these notifications are emitted when
        the status of one of the requested instruments changes

        Parameters
        ----------
        func : Callable, optional
            Callable object to process retrieved status data

        Returns
        -------
        OMMStream
            current instance is an OMM stream object.

        Examples
        --------
        Prerequisite: The default session must be opened.
        >>> from datetime import datetime
        >>> from refinitiv.data.delivery import omm_stream
        >>>
        >>> def display_response(event, stream):
        ...     print(f'Status received at {datetime.now}')
        ...     print(event)
        >>>
        >>> definition = omm_stream.Definition("EUR")
        >>> stream = definition.get_stream()
        >>> stream.on_status(display_response)
        >>>
        >>> stream.open()
        """
        self._stream.on_status(func)
        return self

    def on_complete(self, func: Callable[[dict, "OMMStream"], Any]) -> "OMMStream":
        """
        This function called on complete event

        Parameters
        ----------
        func : Callable, optional
            Callable object to process when retrieved on complete data.

        Returns
        -------
        OMMStream
            current instance is an OMM stream object.

        Examples
        --------
        Prerequisite: The default session must be opened.
        >>> from datetime import datetime
        >>> from refinitiv.data.delivery import omm_stream
        >>>
        >>> def display_response(event, stream):
        ...     print(f'Complete received at {datetime.now}')
        ...     print(event)
        >>>
        >>> definition = omm_stream.Definition("EUR")
        >>> stream = definition.get_stream()
        >>> stream.on_complete(display_response)
        >>>
        >>> stream.open()
        """
        self._stream.on_complete(func)
        return self

    def on_error(self, func: Callable[[dict, "OMMStream"], Any]) -> "OMMStream":
        """
        This function called when an error occurs

        Parameters
        ----------
        func : Callable, optional
            Callable object to process when retrieved error data.

        Returns
        -------
        OMMStream
            current instance is an OMM stream object.

        Examples
        --------
        Prerequisite: The default session must be opened.
        >>> from datetime import datetime
        >>> from refinitiv.data.delivery import omm_stream
        >>>
        >>> def display_response(event, response):
        ...     print(f'Error received at {datetime.now}')
        ...     print(event)
        >>>
        >>> definition = omm_stream.Definition("EUR")
        >>> stream = definition.get_stream()
        >>> stream.on_error(display_response)
        >>>
        >>> stream.open()
        """
        self._stream.on_error(func)
        return self

    def on_ack(self, on_ack: Callable[[dict, "OMMStream"], Any]) -> "OMMStream":
        """
        This function called when the stream received an ack message after sending a contribution .

        Parameters
        ----------
        on_ack : Callable, optional
             Callable object to process retrieved ack data

        Returns
        -------
        OMMStream
            current instance is an OMM stream object.

        Examples
        --------
        Prerequisite: The default session must be opened.
        >>> from datetime import datetime
        >>> from refinitiv.data.delivery import omm_stream
        >>>
        >>> def display_response(response, event_type, event):
        ...     print(f'{response} - {event_type} received at {datetime.now}')
        ...     print(event)
        >>>
        >>> definition = omm_stream.Definition("EUR")
        >>> stream = definition.get_stream()
        >>> stream.on_ack(lambda event, stream: display_response(stream, 'ack', event))
        >>>
        >>> stream.open()
        >>> stream.contribute({"ASK": 123, "BID": 125})
        """
        self._stream.on_ack(on_ack)
        return self

    def __repr__(self):
        return create_repr(self, middle_path="omm_stream", class_name=self.__class__.__name__)

    def contribute(
        self, fields: dict, contrib_type: "OptContribT" = None, post_user_info: "OptDict" = None
    ) -> "ContribResponse":
        """
        Function to send OnStream contribution request.

        Parameters
        ----------
        fields: dict{field:value}
            Specify fields and values to contribute.

        contrib_type: Union[str, ContribType], optional
            Define the contribution type
            Default: "Update"

        post_user_info: dict, optional
            PostUserInfo object Represents information about the posting user.
                Address: string, required
                    Dotted-decimal string representing the IP Address of the posting user.
                UserID: int, required
                    Specifies the ID of the posting user

        Returns
        -------
        ContribResponse

        Examples
        --------
        Prerequisite: The default session must be opened.
        >>> from datetime import datetime
        >>> from refinitiv.data.delivery import omm_stream
        >>>
        >>> def display_response(response, event_type, event):
        ...     print(f'{response} - {event_type} received at {datetime.now}')
        ...     print(event)
        >>>
        >>> definition = omm_stream.Definition("EUR")
        >>> stream = definition.get_stream()
        >>> stream.on_ack(lambda event, stream: display_response(stream, 'ack', event))
        >>>
        >>> stream.open()
        >>> response = stream.contribute({"ASK": 123, "BID": 125})
        """
        return self._stream.contribute(fields, contrib_type=contrib_type, post_user_info=post_user_info)

    async def contribute_async(
        self,
        fields: dict,
        contrib_type: "OptContribT" = None,
        post_user_info: "OptDict" = None,
    ) -> "ContribResponse":
        """
        Function to send asynchronous OnStream contribution request.

        Parameters
        ----------
        fields: dict{field:value}
            Specify fields and values to contribute.

        contrib_type: Union[str, ContribType], optional
            Define the contribution type
            Default: "Update"

        post_user_info: dict, optional
            PostUserInfo object Represents information about the posting user.
                Address: string, required
                    Dotted-decimal string representing the IP Address of the posting user.
                UserID: int, required
                    Specifies the ID of the posting user

        Returns
        -------
        ContribResponse

        Examples
        --------
        Prerequisite: The default session must be opened.
        >>> from datetime import datetime
        >>> from refinitiv.data.delivery import omm_stream
        >>> import asyncio
        >>>
        >>> def display_response(response, event_type, event):
        ...     print(f'{response} - {event_type} received at {datetime.now}')
        ...     print(event)
        >>>
        >>> definition = omm_stream.Definition("EUR")
        >>> stream = definition.get_stream()
        >>> stream.on_ack(lambda event, stream: display_response(stream, 'ack', event))
        >>>
        >>> stream.open()
        >>> response = asyncio.run(stream.contribute_async({"ASK": 123, "BID": 125}))
        """
        return await self._stream.contribute_async(fields, contrib_type=contrib_type, post_user_info=post_user_info)
