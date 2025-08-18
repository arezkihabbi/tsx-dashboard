import abc

from ._custom_instruments_data_provider import (
    simple_custom_insts_body_params_config,
    custom_inst_type_arg_parser,
)
from ._enums import CustomInstrumentTypes
from ._instrument_prop_classes import Basket, UDC
from ..._content_type import ContentType
from ..._core.session import Session
from ...delivery._data._data_provider import DataProviderLayer
from ...delivery._data._endpoint_data import RequestMethod


class Instrument(abc.ABC):
    def __init__(self, data: dict, session: "Session" = None):
        """
        symbol : str
            Instrument symbol in the format "S)someSymbol.YOURUUID" or "someSymbol"
        formula : str, optional
            Formula consisting of rics (fields can be specified by comma).
        basket : dict, Basket, optional
            For weighted baskets / indices.
        udc : dict, UDC, optional
            Custom trading sessions, see sample format below.
        instrument_name : str, optional
            Human-readable name of the instrument. Maximum of 16 characters.
        exchange_name : str, optional
            4-letter code of the listing exchange.
        currency : str, optional
            3-letter code of the currency of the instrument, e.g. GBP.
        time_zone: str, optional
            Time Series uses an odd custom 3-letter value for time zone IDs, e.g. "LON" for London.
        holidays : List[Union[dict, Holiday]], optional
            List of custom calendar definitions.
        description : str, optional
            Free text field from the user to put any notes or text. Up to 1000 characters.
        session : Session, optional
            session=None - means default session would be used

        """
        self._data = data
        self._session = session

    @property
    def raw(self):
        return self._data

    @property
    def symbol(self):
        return self._data.get("symbol")

    @symbol.setter
    def symbol(self, value):
        self._data["symbol"] = value

    @property
    def instrument_name(self):
        return self._data.get("instrumentName")

    @instrument_name.setter
    def instrument_name(self, value):
        self._data["instrumentName"] = value

    @property
    def exchange_name(self):
        return self._data.get("exchangeName")

    @exchange_name.setter
    def exchange_name(self, value):
        self._data["exchangeName"] = value

    @property
    def currency(self):
        return self._data.get("currency")

    @currency.setter
    def currency(self, value):
        self._data["currency"] = value

    @property
    def time_zone(self):
        return self._data.get("timeZone")

    @time_zone.setter
    def time_zone(self, value):
        self._data["timeZone"] = value

    @property
    def holidays(self):
        return self._data.get("holidays")

    @holidays.setter
    def holidays(self, value):
        self._data["holidays"] = value

    @property
    def description(self):
        return self._data.get("description")

    @description.setter
    def description(self, value):
        self._data["description"] = value

    @property
    def id(self):
        return self._data.get("id")

    @property
    def owner(self):
        return self._data.get("owner")

    @property
    def type_(self):
        return self._data.get("type")

    def delete(self):
        """
        Examples
        --------
        >>> from refinitiv.data.content.custom_instruments.manage import get
        >>> instrument = get("MyInstrument")
        >>> instrument.delete()
        """
        data_provider_layer = DataProviderLayer(
            data_type=ContentType.CUSTOM_INSTRUMENTS_INSTRUMENTS,
            universe=self.symbol,
            method=RequestMethod.DELETE,
        )
        data_provider_layer.get_data(self._session)

    def save(self):
        """
        Examples:
        --------
        >>> from refinitiv.data.content.custom_instruments.manage import create_formula, Holiday
        >>> instrument = create_formula(
        ...     symbol="MyNewInstrument",
        ...     formula="EUR=*3",
        ...     holidays=[
        ...         Holiday(date="1991-08-23", name="Independence Day of Ukraine"),
        ...         {"date": "2022-12-18", "reason": "Hanukkah"},
        ...     ],
        ... )
        ... instrument.currency = "GBP"
        ... instrument.description = "short trading instrument"
        ... instrument.exchange_name = "9978"
        ... instrument.save()
        """
        provider = DataProviderLayer(
            data_type=ContentType.CUSTOM_INSTRUMENTS_INSTRUMENTS,
            universe=self.id,
            body_params_config=simple_custom_insts_body_params_config,
            method=RequestMethod.PUT,
            **self._data,
        )
        response = provider.get_data(self._session)
        self._data = response.data.raw


class CustomInstrumentFormula(Instrument):
    @property
    def formula(self):
        return self._data.get("formula")

    @formula.setter
    def formula(self, value):
        self._data["formula"] = value


class CustomInstrumentBasket(Instrument):
    @property
    def basket(self):
        return Basket._from_dict(self._data.get("basket"))

    @basket.setter
    def basket(self, value):
        self._data["basket"] = value


class CustomInstrumentUDC(Instrument):
    @property
    def udc(self) -> UDC:
        return UDC._from_dict(self._data.get("udc"))

    @udc.setter
    def udc(self, value):
        self._data["udc"] = value


class_by_type = {
    CustomInstrumentTypes.Formula: CustomInstrumentFormula,
    CustomInstrumentTypes.Basket: CustomInstrumentBasket,
    CustomInstrumentTypes.UDC: CustomInstrumentUDC,
}


def create_instr_factory(data, session):
    _type = data.get("type")

    if not _type:
        raise AttributeError("type parameter is not existed for object")

    enum_type = custom_inst_type_arg_parser.get_enum(_type)
    _class = class_by_type.get(enum_type)

    if not _class:
        raise AttributeError(f"There is no valid class for {enum_type}")

    ci = _class(data, session=session)
    return ci
