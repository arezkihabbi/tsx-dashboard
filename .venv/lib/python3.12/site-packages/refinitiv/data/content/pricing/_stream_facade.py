from typing import TYPE_CHECKING, Any, Callable, List, Optional, Union

from .._universe_streams import UniverseStreamFacade, _UniverseStreams
from ..._content_type import ContentType
from ..._core.session import get_valid_session
from ..._tools import PRICING_DATETIME_PATTERN, cached_property, create_repr
from ..._tools._dataframe import convert_df_columns_to_datetime_re
from ..._types import OptStr, Strings, OptDict
from ...delivery._stream import StreamOpenWithUpdatesMixin, OptContribT

if TYPE_CHECKING:
    import pandas

    from ... import OpenState
    from ..._core.session import Session
    from ...delivery.omm_stream import ContribResponse


class PricingStream(UniverseStreamFacade):
    pass


class Stream(StreamOpenWithUpdatesMixin):
    """
    Summary line of this class are used for requesting, processing and managing a set of
    streaming level 1 (MarketPrice domain) quotes and trades

    Extended description of this class:
        The object automatically manages a set of streaming caches available for access
        at any time. Your application can then reach into this cache and pull out
        real-time fields by just calling a simple access method.
        The object also emits a number of different events, your application can
        listen to in order to be notified of the latest field values in real-times.
        The object iterable.

    Parameters
    ----------
    session : Session, optional
        Means default session would be used
    universe : str or list of str, optional
        The single/multiple instrument/s name (e.g. "EUR=" or ["EUR=", "CAD=", "UAH="])
    fields : list, optional
        Specifies the specific fields to be delivered when messages arrive
    service : str, optional
        Name of the streaming service publishing the instruments
    api: str, optional
        Specifies the data source. It can be updated/added using config file
    extended_params : dict, optional
        If necessary other parameters

    Examples
    --------
    >>> from refinitiv.data.content import pricing
    >>> definition = pricing.Definition("EUR=")
    >>> stream = definition.get_stream()
    """

    def __init__(
        self,
        session: "Session" = None,
        universe: Union[str, List[str]] = None,
        fields: Optional[list] = None,
        service: OptStr = None,
        api: OptStr = None,
        extended_params: Optional[dict] = None,
    ) -> None:
        self._session = get_valid_session(session)
        self._always_use_default_session = session is None
        self._universe = universe or []
        self._fields = fields
        self._service = service
        self._api = api
        self._extended_params = extended_params

    @cached_property
    def _stream(self) -> _UniverseStreams:
        return _UniverseStreams(
            content_type=ContentType.STREAMING_PRICING,
            item_facade_class=PricingStream,
            universe=self._universe,
            session=self._session,
            fields=self._fields,
            service=self._service,
            api=self._api,
            extended_params=self._extended_params,
            owner=self,
        )

    def open(self, with_updates: bool = True) -> "OpenState":
        """
        Opens the streaming connection to the Pricing data, and sends corresponding requests for all requested
        instruments.

         It will be opened once all the requested instruments are received
         either on_refresh, on_status or other method.
         Then the pricing.stream can be used in order to retrieve data.

        Parameters
        ----------
        with_updates : bool, optional
            Boolean indicator of how to work with the stream. If True - all data will be received continuously. If
            False - only the data snapshot will be received.

        Returns
        -------
        OpenState

        Examples
        --------
        >>> from refinitiv.data.content import pricing
        >>> definition = pricing.Definition("EUR=")
        >>> stream = definition.get_stream()
        >>> stream.open()
        """
        return super().open(with_updates=with_updates)

    def close(self) -> "OpenState":
        """
        Closes the streaming connection to the Pricing data.

        Returns
        -------
        OpenState

        Examples
        --------
        >>> from refinitiv.data.content import pricing
        >>> definition = pricing.Definition("EUR=")
        >>> stream = definition.get_stream()
        >>> stream.open()
        >>> stream.close()
        """
        return super().close()

    def _get_fields(self, universe: str, fields: Optional[list] = None) -> dict:
        """
        Returns a dict of the fields for a requested universe.

        Parameters
        ----------
        universe: str
            Name of the instrument (e.g. 'EUR=' ...).
        fields: list, optional
            The fields that are listed in the `fields` parameter.

        Returns
        -------
        dict

        Examples
        --------
        >>> from refinitiv.data.content import pricing
        >>> definition = pricing.Definition(["AIRP.PA", "AIR.PA", "ALSO.PA"])
        >>> stream = definition.get_stream()
        >>> fields
        ... {'AIRP.PA': {'BID': 147.14, 'ASK': 147.16}}
        """
        _fields = {
            universe: {key: value for key, value in self._stream[universe].items() if fields is None or key in fields}
        }
        return _fields

    def get_snapshot(
        self,
        universe: Optional[Union[str, Strings]] = None,
        fields: Optional[Union[str, Strings]] = None,
        convert: bool = True,
    ) -> "pandas.DataFrame":
        """
        Returns a snapshot of the instruments stored in the in-memory data cache of the stream. When the stream is
        opened, this data cache is kept up-to-date with the latest updates received from the platform.

        Parameters
        ----------
        universe: str, list of str, optional
            Single instrument or list of instruments.

        fields: str, list of str, optional
            Single field or list of fields to return.

        convert: bool, optional
            If True - force numeric conversion to all values.

        Returns
        -------
            pandas.DataFrame

            pandas.DataFrame content:
                - columns : instrument and fieled names
                - rows : instrument name and field values

        Raises
        ------
            Exception
                If request fails or if server returns an error

            ValueError
                If a parameter type or value is wrong

        Examples
        --------
        >>> from refinitiv.data.content import pricing
        >>> definition = pricing.Definition(
        ...    ["MSFT.O", "GOOG.O", "IBM.N"],
        ...    fields=["BID", "ASK", "OPEN_PRC"]
        ...)
        >>> stream = definition.get_stream()
        >>> data = stream.get_snapshot(["MSFT.O", "GOOG.O"], ["BID", "ASK"])
        >>> data
        ... "      Instrument   BID         ASK      "
        ... "0     MSFT.O        150.9000   150.9500 "
        ... "1     GOOG.O        1323.9000  1327.7900"
        """
        df = self._stream.get_snapshot(universe=universe, fields=fields, convert=convert)
        convert_df_columns_to_datetime_re(df, PRICING_DATETIME_PATTERN)
        return df

    def on_refresh(self, func: Callable[[Any, str, "Stream"], Any]) -> "Stream":
        """
        Called every time the whole fields list of a requested instrument is received from the platform.

        Parameters
        ----------
        func : Callable
            Callable object to process the retrieved data.

        Returns
        -------
        current instance

        Examples
        --------
        >>> import datetime
        >>> from refinitiv.data.content import pricing
        >>> definition = pricing.Definition("EUR=")
        >>> stream = definition.get_stream()
        >>> def on_refresh(message, ric, stream):
        ...    current_time = datetime.datetime.now().time()
        ...    print("\t{} | Receive refresh [{}] : {}".format(current_time, ric, message))  # noqa
        >>> stream.on_refresh(on_refresh)
        >>> stream.open()
        """
        self._stream.on_refresh(func)
        return self

    def on_update(self, func: Callable[[Any, str, "Stream"], Any]) -> "Stream":
        """
        Called when some fields of one of the requested instruments are updated.

        Parameters
        ----------
        func : Callable
            Callable object to process the retrieved data

        Returns
        -------
        current instance

        Examples
        --------
        >>> import datetime
        >>> from refinitiv.data.content import pricing
        >>> definition = pricing.Definition("EUR=")
        >>> stream = definition.get_stream()
        >>> def on_update(update, ric, stream):
        ...     current_time = datetime.datetime.now().time()
        ...     print("\t{} | Receive update [{}] : {}".format(current_time, ric, update))  # noqa
        >>> stream.on_update(on_update)
        >>> stream.open()
        """
        self._stream.on_update(func)
        return self

    def on_status(self, func: Callable[[Any, str, "Stream"], Any]) -> "Stream":
        """
        Called when a status is received for one of the requested instruments.

        Parameters
        ----------
        func : Callable
            Callable object to process the retrieved data.

        Returns
        -------
        current instance

        Examples
        --------
        >>> from refinitiv.data.content import pricing
        >>> definition = pricing.Definition("EUR=")
        >>> stream = definition.get_stream()
        >>> def on_status(status, ric, stream):
        ...     print("\tReceive status [{}] : {}".format(ric, status))
        >>> stream.on_status(on_status)
        >>> stream.open()
        """
        self._stream.on_status(func)
        return self

    def on_complete(self, func: Callable[["Stream"], Any]) -> "Stream":
        """
        Called after the requested instruments and fields are completely received. on_complete is only called once
        per stream opening.

        Parameters
        ----------
        func : Callable
            Callable object to process the retrieved data

        Returns
        -------
        current instance

        Examples
        --------
        >>> import datetime
        >>> from refinitiv.data.content import pricing
        >>> definition = pricing.Definition("EUR=")
        >>> stream = definition.get_stream()
        >>> def on_complete(stream):
        ...    current_time = datetime.datetime.now().time()
        ...    print("\t{} | Receive complete".format(current_time))
        >>> stream.on_complete(on_complete)
        >>> stream.open()
        """
        self._stream.on_complete(func)
        return self

    def on_error(self, func: Callable[[Any, str, "Stream"], Any]) -> "Stream":
        self._stream.on_error(func)
        return self

    def on_ack(self, func: Callable[[Any, str, "Stream"], Any]) -> "Stream":
        """
        Called when a data retrieval error happens.

        Parameters
        ----------
        func : Callable, optional
             Callable object to process the retrieved data.

        Returns
        -------
        Stream
            current instance

        Examples
        --------
        Prerequisite: The default session must be opened.

        >>> from refinitiv.data.content import pricing
        >>>
        >>> definition = pricing.Definition("EUR=")
        >>> stream = definition.get_stream()
        >>> def on_ack(ack_msg, ric, stream):
        ...     print(f"\tReceive ack [{ric}] : {ack_msg}")
        >>> stream.on_ack(on_ack)
        >>> stream.open()
        >>> result = stream.contribute("EUR=", {"BID": 1.12})
        """
        self._stream.on_ack(func)
        return self

    def contribute(
        self, name: str, fields: dict, contrib_type: OptContribT = None, post_user_info: OptDict = None
    ) -> "ContribResponse":
        """
        Function to send OnStream contribution request.

        Parameters
        ----------
        name: string
            RIC to contribute to.

        fields: dict{field:value}
            Specify fields and values to contribute.

        contrib_type: Union[str, ContribType], optional
            Define the contribution type.
            Default: "Update"

        post_user_info: dict, optional
            PostUserInfo object represents information about the posting user.
                Address: string, required
                    Dotted-decimal string representing the IP Address of the posting user.
                UserID: int, required
                    Specifies the ID of the posting user

        Returns
        -------
        ContribResponse

        Examples
        --------
        >>> import refinitiv.data as rd
        >>>
        >>> pricing_stream = rd.content.pricing.Definition(
        ...    ["MSFT.O", "GOOG.O", "IBM.N"],
        ...    fields=["BID", "ASK", "OPEN_PRC"]
        ...).get_stream()
        >>> response = pricing_stream.contribute("MSFT.O", {"BID": 240.83})
        """
        return self._stream.contribute(name, fields, contrib_type, post_user_info)

    async def contribute_async(
        self, name: str, fields: dict, contrib_type: OptContribT = None, post_user_info: OptDict = None
    ) -> "ContribResponse":
        """
        Function to send asynchronous OnStream contribution request.

        Parameters
        ----------
        name: string
            RIC to contribute to.

        fields: dict{field:value}
            Specify fields and values to contribute.

        contrib_type: Union[str, ContribType], optional
            Define the contribution type.
            Default: "Update"

        post_user_info: dict, optional
            PostUserInfo object represents information about the posting user.
                Address: string, required
                    Dotted-decimal string representing the IP Address of the posting user.
                UserID: int, required
                    Specifies the ID of the posting user

        Returns
        -------
        ContribResponse

        Examples
        --------
        >>> import refinitiv.data as rd
        >>> import asyncio
        >>> pricing_stream = rd.content.pricing.Definition(
        ...    ["MSFT.O", "GOOG.O", "IBM.N"],
        ...    fields=["BID", "ASK", "OPEN_PRC"]
        ...).get_stream()
        >>> response = asyncio.run(pricing_stream.contribute_async("MSFT.O", {"BID": 240.83}))
        """
        return await self._stream.contribute_async(name, fields, contrib_type, post_user_info)

    def add_instruments(self, instruments) -> None:
        """
        Add instruments to the stream universe.

        Parameters
        ----------
        instruments: str, list of str, optional
            List of instruments to add.

        Examples
        --------
        >>> from refinitiv.data.content import pricing
        >>> definition = pricing.Definition(
        ...    ["MSFT.O", "GOOG.O", "IBM.N"],
        ...)
        >>> stream = definition.get_stream()
        >>> stream.add_instruments("VOD.L")
        """
        self._stream.add_instruments(instruments)

    def remove_instruments(self, instruments) -> None:
        """
        Remove instruments from the stream universe.

        Parameters
        ----------
        instruments: str, list of str, optional
            List of instruments to remove.

        Examples
        --------
        >>> from refinitiv.data.content import pricing
        >>> definition = pricing.Definition(
        ...    ["MSFT.O", "GOOG.O", "IBM.N"],
        ...)
        >>> stream = definition.get_stream()
        >>> stream.remove_instruments("GOOG.O")
        """
        self._stream.remove_instruments(instruments)

    def add_fields(self, fields) -> None:
        """
        Add fields to the fields list.

        Parameters
        ----------
        fields: str, list of str, optional
            List of fields to add.

        Examples
        --------
        >>> from refinitiv.data.content import pricing
        >>> definition = pricing.Definition(
        ...    ["MSFT.O", "GOOG.O", "IBM.N"],
        ...    fields=["BID", "ASK", "OPEN_PRC"]
        ...)
        >>> stream = definition.get_stream()
        >>> stream.add_fields("TRDPRC_1")
        """
        self._stream.add_fields(fields)

    def remove_fields(self, fields) -> None:
        """
        Remove fields from the fields list.

        Parameters
        ----------
        fields: str, list of str, optional
            List of fields to remove.

        Examples
        --------
        >>> from refinitiv.data.content import pricing
        >>> definition = pricing.Definition(
        ...    ["MSFT.O", "GOOG.O", "IBM.N"],
        ...    fields=["BID", "ASK", "OPEN_PRC"]
        ...)
        >>> stream = definition.get_stream()
        >>> stream.remove_fields("ASK")
        """
        self._stream.remove_fields(fields)

    def __iter__(self):
        return self._stream.__iter__()

    def __getitem__(self, item) -> "PricingStream":
        return self._stream.__getitem__(item)

    def __len__(self) -> int:
        return self._stream.__len__()

    def __repr__(self):
        return create_repr(self, class_name=self.__class__.__name__, content=f"{{name='{self._universe}'}}")
