from typing import Any, Callable, List, Optional, TYPE_CHECKING

from ._custom_instruments_data_provider import (
    is_instrument_id,
    get_valid_symbol,
    get_valid_symbol_request,
    symbol_with_user_id,
)
from ..._core.session.tools import get_user_id
from .._universe_stream import _UniverseStream
from .._universe_streams import UniverseStreamFacade, _UniverseStreams
from ..._content_type import ContentType
from ..._core.session import get_valid_session
from ..._tools import (
    PRICING_DATETIME_PATTERN,
    cached_property,
    create_repr,
    convert_df_columns_to_datetime_re,
    universe_arg_parser,
)
from ...delivery._data._data_provider import DataProviderLayer
from ...delivery._data._endpoint_data import RequestMethod
from ...delivery._stream import StreamOpenWithUpdatesMixin

if TYPE_CHECKING:
    from ..._types import OptStr, StrStrings, Strings, OptStrStrs, ExtendedParams
    import pandas
    from ..._core.session import Session


def uuid_from_symbol(symbol: str) -> str:
    if "." in symbol:
        return symbol.rsplit(".", 1)[-1]
    else:
        return ""


def get_symbols_by_universe(universe: "StrStrings", session: "Session", uuid=None) -> "Strings":
    data_provider_layer = DataProviderLayer(
        data_type=ContentType.CUSTOM_INSTRUMENTS_INSTRUMENTS,
        universe=universe,
    )

    symbols = []
    for item in universe:
        # a20140be-3648-4892-9d1b-ce78ee8617fd
        if is_instrument_id.match(item):
            instrument_response = data_provider_layer.get_data(session, method=RequestMethod.GET)
            # S)MyNewInstrument5.GE-1525-0
            symbol = instrument_response.data.raw.get("symbol")

        else:
            # S)MyNewInstrument5
            if not symbol_with_user_id.match(item) and not uuid:
                # S)MyNewInstrument5.GE-1525-0
                symbol = get_valid_symbol_request(item, session)
                # GE-1525-0
                uuid = uuid_from_symbol(symbol)

            else:
                symbol = get_valid_symbol(item, uuid)

        symbols.append(symbol)

    return symbols


class CustomInstrumentsStream(UniverseStreamFacade):
    pass


class CustomInstsUniverseStream(_UniverseStream):
    def filter_fields(self, fields):
        prv_fields = self._fields or []
        return {k: v for k, v in fields.items() if k in prv_fields}


class CustomInstsUniverseStreams(_UniverseStreams):
    def create_stream_by_name(self, name: str) -> CustomInstsUniverseStream:
        return CustomInstsUniverseStream(
            content_type=self._content_type,
            session=self._session,
            name=name,
            fields=self.fields,
            service=self._service,
            api=self._api,
            extended_params=self._extended_params,
            owner=self,
        )


class Stream(StreamOpenWithUpdatesMixin):
    def __init__(
        self,
        session: "Session" = None,
        universe: "OptStrStrs" = None,
        fields: Optional[list] = None,
        service: "OptStr" = None,
        api: "OptStr" = None,
        extended_params: "ExtendedParams" = None,
        uuid: "OptStr" = None,
    ) -> None:
        self._session = get_valid_session(session)
        self._always_use_default_session = session is None
        self._universe = universe or []
        self._fields = fields
        self._service = service
        self._api = api
        self._extended_params = extended_params

        if not uuid:
            uuid = get_user_id(self._session)
        self._uuid = uuid

    @cached_property
    def _stream(self) -> _UniverseStreams:
        return CustomInstsUniverseStreams(
            content_type=ContentType.STREAMING_CUSTOM_INSTRUMENTS,
            item_facade_class=CustomInstrumentsStream,
            universe=self._universe,
            session=self._session,
            fields=self._fields,
            service=self._service,
            api=self._api,
            extended_params=self._extended_params,
        )

    def _get_fields(self, universe: str, fields: Optional[list] = None) -> dict:
        _fields = {
            universe: {key: value for key, value in self._stream[universe].items() if fields is None or key in fields}
        }
        return _fields

    def get_snapshot(
        self, universe: "OptStrStrs" = None, fields: Optional[List[str]] = None, convert: bool = True
    ) -> "pandas.DataFrame":
        universe = universe_arg_parser.get_list(universe or [])
        universe = [get_valid_symbol(i, self._uuid) for i in universe]
        df = self._stream.get_snapshot(universe=universe, fields=fields, convert=convert)
        convert_df_columns_to_datetime_re(df, PRICING_DATETIME_PATTERN)
        return df

    def on_refresh(self, func: Callable[[Any, str, "Stream"], Any]) -> "Stream":
        self._stream.on_refresh(func)
        return self

    def on_update(self, func: Callable[[Any, str, "Stream"], Any]) -> "Stream":
        self._stream.on_update(func)
        return self

    def on_status(self, func: Callable[[Any, str, "Stream"], Any]) -> "Stream":
        self._stream.on_status(func)
        return self

    def on_complete(self, func: Callable[["Stream"], Any]) -> "Stream":
        self._stream.on_complete(func)
        return self

    def on_error(self, func: Callable[[Any, str, "Stream"], Any]) -> "Stream":
        self._stream.on_error(func)
        return self

    def add_fields(self, fields):
        """
        Add fields to the fields list.

        Parameters
        ----------
        fields: str, list of str, optional
            List of fields to add.

        Examples
        --------
        >>> from refinitiv.data.content import custom_instruments
        >>> definition = custom_instruments.Definition(
        ...    ["Instrument1", "Instrument2", "Instrument3"],
        ...    fields=["TRDPRC_1", "ASK"]
        ...)
        >>> stream = definition.get_stream()
        >>> stream.add_fields("BID")
        """
        self._stream.add_fields(fields)

    def remove_fields(self, fields):
        """
        Remove fields from the fields list.

        Parameters
        ----------
        fields: str, list of str, optional
            List of fields to remove.

        Examples
        --------
        >>> from refinitiv.data.content import custom_instruments
        >>> definition = custom_instruments.Definition(
        ...    ["Instrument1", "Instrument2", "Instrument3"],
        ...    fields=["TRDPRC_1", "ASK"]
        ...)
        >>> stream = definition.get_stream()
        >>> stream.remove_fields("ASK")
        """
        self._stream.remove_fields(fields)

    def add_instruments(self, instruments: "StrStrings"):
        """
        Add instruments to the stream universe.

        Parameters
        ----------
        instruments: str, list of str
            List of instruments to add.

        Examples
        --------
        >>> from refinitiv.data.content import custom_instruments
        >>> definition = custom_instruments.Definition(
        ...    ["Instrument1", "Instrument2", "Instrument3"],
        ...)
        >>> stream = definition.get_stream()
        >>> stream.add_instruments("Instrument4")
        """
        self._stream.add_instruments(get_symbols_by_universe(universe_arg_parser.get_list(instruments), self._session))

    def remove_instruments(self, instruments: "StrStrings"):
        """
        Remove instruments from the stream universe.

        Parameters
        ----------
        instruments: str, list of str
            List of instruments to remove.

        Examples
        --------
        >>> from refinitiv.data.content import custom_instruments
        >>> definition = custom_instruments.Definition(
        ...    ["Instrument1", "Instrument2", "Instrument3"],
        ...)
        >>> stream = definition.get_stream()
        >>> stream.remove_instruments("Instrument2")
        """
        self._stream.remove_instruments(
            get_symbols_by_universe(universe_arg_parser.get_list(instruments), self._session)
        )

    def __iter__(self):
        return self._stream.__iter__()

    def __getitem__(self, item) -> "UniverseStreamFacade":
        return self._stream.__getitem__(get_valid_symbol(item, self._uuid))

    def __len__(self) -> int:
        return self._stream.__len__()

    def __repr__(self):
        return create_repr(self, class_name=self.__class__.__name__, content=f"{{name='{self._universe}'}}")
