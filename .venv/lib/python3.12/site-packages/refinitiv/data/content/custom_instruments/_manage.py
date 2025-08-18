from typing import Optional, List, Union, Callable, TYPE_CHECKING

from ._enums import CustomInstrumentTypes
from ._instrument_class import (
    create_instr_factory,
    CustomInstrumentFormula,
    CustomInstrumentBasket,
    CustomInstrumentUDC,
)
from ._instrument_prop_classes import Basket, UDC
from ..ipa.dates_and_calendars.holidays._holidays_data_provider import Holiday
from ..._content_type import ContentType
from ..._core.session import Session
from ...delivery._data._data_provider import DataProviderLayer, Response
from ...delivery._data._endpoint_data import RequestMethod

if TYPE_CHECKING:
    from ..._types import ExtendedParams


def delete(
    universe: str,
    extended_params: "ExtendedParams" = None,
    session: "Session" = None,
) -> Response:
    """
    universe : str
        Instrument symbol in the format "S)someSymbol.YOURUUID".
    extended_params : ExtendedParams, optional
        If necessary other parameters.
    session : Session, optional
        session=None. Means default session would be used

    Examples
    --------
    >>> from refinitiv.data.content.custom_instruments.manage import delete
    >>> response = delete("MyInstrument")
    """
    data_provider_layer = DataProviderLayer(
        data_type=ContentType.CUSTOM_INSTRUMENTS_INSTRUMENTS,
        universe=universe,
        extended_params=extended_params,
        method=RequestMethod.DELETE,
    )
    return data_provider_layer.get_data(session)


def get(
    universe: str, extended_params: "ExtendedParams" = None, session: "Session" = None
) -> Union[CustomInstrumentFormula, CustomInstrumentBasket, CustomInstrumentUDC]:
    """
    universe : str
        Instrument symbol in the format "S)someSymbol.YOURUUID".
    extended_params : ExtendedParams, optional
        If necessary other parameters.
    session : Session, optional
        session=None - means default session would be used

    Examples
    --------
    >>> from refinitiv.data.content.custom_instruments.manage import get
    >>> response = get("MyInstrument")
    """
    data_provider_layer = DataProviderLayer(
        data_type=ContentType.CUSTOM_INSTRUMENTS_INSTRUMENTS,
        universe=universe,
        method=RequestMethod.GET,
        extended_params=extended_params,
    )
    response = data_provider_layer.get_data(session=session)
    return create_instr_factory(response.data.raw, session=session)


def _create(
    symbol: str,
    formula: Optional[str] = None,
    basket: Union[dict, Basket] = None,
    udc: Union[dict, UDC] = None,
    instrument_name: Optional[str] = None,
    exchange_name: Optional[str] = None,
    currency: Optional[str] = None,
    time_zone: Optional[str] = None,
    holidays: Optional[List[Union[dict, Holiday]]] = None,
    description: Optional[str] = None,
    type_: Union[str, CustomInstrumentTypes] = None,
    extended_params: "ExtendedParams" = None,
    session: "Session" = None,
    on_response: Callable = None,
) -> dict:
    data_provider_layer = DataProviderLayer(
        data_type=ContentType.CUSTOM_INSTRUMENTS_INSTRUMENTS,
        symbol=symbol,
        formula=formula,
        instrument_name=instrument_name,
        exchange_name=exchange_name,
        currency=currency,
        time_zone=time_zone,
        holidays=holidays,
        description=description,
        type_=type_,
        basket=basket,
        udc=udc,
        extended_params=extended_params,
        method=RequestMethod.POST,
    )
    response = data_provider_layer.get_data(session, on_response)
    return response.data.raw


def create_formula(
    symbol: str,
    formula: Optional[str] = None,
    currency: Optional[str] = None,
    instrument_name: Optional[str] = None,
    exchange_name: Optional[str] = None,
    holidays: Optional[List[Union[dict, Holiday]]] = None,
    time_zone: Optional[str] = None,
    description: Optional[str] = None,
    extended_params: "ExtendedParams" = None,
    session: "Session" = None,
    on_response: Callable = None,
) -> CustomInstrumentFormula:
    """
    With this method you can create a CustomInstrumentFormula object.

    Parameters
    ----------
    symbol: str
        Instrument symbol in the format "S)someSymbol.YOURUUID".
    formula : str
        Formula consisting of rics (fields can be specified by comma).
    currency : str, optional
        3-letter code of the currency of the instrument, e.g. GBP.
    instrument_name : str, optional
        Human-readable name of the instrument. Maximum of 16 characters.
    exchange_name : str, optional
        4-letter code of the listing exchange.
    holidays : list[dict, Holiday], optional
        List of custom calendar definitions.
    time_zone : str, optional
        Time Series uses an odd custom 3-letter value for time zone IDs, e.g. "LON" for London.
    description : str, optional
        Free text field from the user to put any notes or text. Up to 1000 characters.
    extended_params : ExtendedParams, optional
        If necessary other parameters.
    session : Session, optional
        session=None - means default session would be used
    on_response : Callable, optional
        Callable object to process retrieved data

    Returns
    -------
        CustomInstrumentFormula

    Examples
    --------
    >>> from refinitiv.data.content.custom_instruments.manage import create_formula
    >>> import refinitiv.data.content.custom_instruments as ci
    >>> response = create_formula(
    ...     symbol="MyNewInstrument",
    ...     formula="EUR=*3",
    ...     holidays=[
    ...         ci.manage.Holiday(date="1991-08-23", name="Independence Day of Ukraine"),
    ...         {"date": "2022-12-18", "reason": "Hanukkah"},
    ...     ],
    >>> )
    """
    data = _create(
        symbol=symbol,
        type_=CustomInstrumentTypes.Formula,
        formula=formula,
        currency=currency,
        instrument_name=instrument_name,
        exchange_name=exchange_name,
        holidays=holidays,
        time_zone=time_zone,
        description=description,
        extended_params=extended_params,
        session=session,
        on_response=on_response,
    )
    return CustomInstrumentFormula(data, session=session)
