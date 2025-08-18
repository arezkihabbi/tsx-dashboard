from typing import TYPE_CHECKING, Union

from ._asset_class import AssetClass
from ._asset_class import (
    create_asset_class_request_strings,
    asset_class_enum_arg_parser,
)
from ._asset_state import AssetState
from ._asset_state import asset_state_enum_arg_parser
from ._country_code import country_code_arg_parser
from ._symbol_type import SYMBOL_TYPE_VALUES, symbol_types_arg_parser
from .._content_provider_layer import ContentProviderLayer
from ..search import Views
from ..._content_type import ContentType
from ..._tools import create_repr, Copier

if TYPE_CHECKING:
    from ._asset_state import OptAssetState
    from ._country_code import OptCountryCode
    from ._symbol_type import SymbolTypesType, OptSymbolTypes
    from ._asset_class import OptAssetClass
    from ._country_code import CountryCode
    from ._symbol_type import SymbolTypes
    from ..._types import ExtendedParams, StrStrings

DEFAULT_SCOPE = "_AllUnique"


def _prepare_filter(asset_state: AssetState, asset_class: Union[list, AssetClass]) -> str:
    asset_state = asset_state or AssetState.ACTIVE

    if asset_state is AssetState.ACTIVE:
        ret_val = "AssetState eq 'AC'"
    else:
        ret_val = "(AssetState ne 'AC' and AssetState ne null)"

    if asset_class and not isinstance(asset_class, list):
        asset_class = [asset_class]

    if asset_class:
        search_all_category, rcs_asset_category = create_asset_class_request_strings(asset_class)

        if search_all_category and rcs_asset_category:
            ret_val = f"{ret_val} and ({search_all_category} or {rcs_asset_category})"
        else:
            ret_val = f"{ret_val} and ({search_all_category}{rcs_asset_category})"

    return ret_val


class Definition(ContentProviderLayer):
    """
    Creates a definition of information about the data that will be passed to the Search/Lookup API of the Refinitiv
    Data Platform.

    Parameters
    ----------
    symbols: str or list of str
        Single instrument or list of instruments to convert.

    from_symbol_type: str or SymbolTypes, optional
        Instrument code to convert from.
        Possible values: 'CUSIP', 'ISIN', 'SEDOL', 'RIC', 'ticker', 'lipperID', 'IMO'
        Default: '_AllUnique'

    to_symbol_types: SymbolTypes, str or list of str or SymbolTypes, optional
        Instrument code to convert to.
        Possible values: 'CUSIP', 'ISIN', 'SEDOL', 'RIC', 'ticker', 'lipperID', 'IMO', 'OAPermID'
        Default: all symbol types are requested

    extended_params: dict, optional
        Specifies the parameters that will be merged with the request.

    preferred_country_code: str or CountryCode, optional
        Unique ISO 3166 code for country

    asset_class: str or AssetClass, optional
        AssetClass value to build filter parameter.

    asset_state: str or AssetState, optional
        AssetState value to build filter parameter.

    Examples
    --------
    >>> from refinitiv.data.content import symbol_conversion
    >>> definition = symbol_conversion.Definition(
    ...     symbols=["US5949181045", "US02079K1079"],
    ...     from_symbol_type=symbol_conversion.SymbolTypes.ISIN,
    ...     to_symbol_types=[
    ...         symbol_conversion.SymbolTypes.RIC,
    ...         symbol_conversion.SymbolTypes.OA_PERM_ID
    ...     ],
    ...     preferred_country_code=symbol_conversion.CountryCode.USA,
    ...     asset_class=[
    ...        symbol_conversion.AssetClass.COMMODITIES,
    ...        symbol_conversion.AssetClass.EQUITIES,
    ...        symbol_conversion.AssetClass.WARRANTS
    ...     ],
    ...     asset_state=symbol_conversion.AssetState.INACTIVE
    ... )
    >>> response = definition.get_data()
    """

    def __init__(
        self,
        symbols: "StrStrings",
        from_symbol_type: Union[str, "SymbolTypes"] = DEFAULT_SCOPE,
        to_symbol_types: "SymbolTypesType" = SYMBOL_TYPE_VALUES,
        preferred_country_code: "OptCountryCode" = None,
        asset_class: "OptAssetClass" = None,
        asset_state: "OptAssetState" = None,
        extended_params: "ExtendedParams" = None,
    ):
        super().__init__(
            content_type=ContentType.DISCOVERY_LOOKUP,
            view=Views.SEARCH_ALL,
        )

        self.symbols = symbols
        self.from_symbol_type = from_symbol_type
        self.to_symbol_types = to_symbol_types
        self.preferred_country_code = preferred_country_code
        self.asset_class = asset_class
        self.asset_state = asset_state
        self.extended_params = extended_params

    @property
    def symbols(self) -> "StrStrings":
        return self._kwargs.get("terms")

    @symbols.setter
    def symbols(self, value: "StrStrings"):
        if value:
            value = Copier.get_list(value)
            self._kwargs["terms"] = ",".join(value)

    @property
    def from_symbol_type(self) -> Union[str, "SymbolTypes"]:
        return self._kwargs.get("scope")

    @from_symbol_type.setter
    def from_symbol_type(self, value: Union[str, "SymbolTypes"]):
        scope = value or DEFAULT_SCOPE
        if value and value != DEFAULT_SCOPE:
            scope = symbol_types_arg_parser.get_str(value)

        self._kwargs["scope"] = scope

    @property
    def to_symbol_types(self) -> "OptSymbolTypes":
        return self._kwargs.get("select")

    @to_symbol_types.setter
    def to_symbol_types(self, value: "OptSymbolTypes"):
        value = value and Copier.get_list(value)
        select = ["DocumentTitle"]

        if value is SYMBOL_TYPE_VALUES:
            select.extend(value)

        elif isinstance(value, list):
            select.extend(map(symbol_types_arg_parser.get_str, value))

        elif value:
            select.append(symbol_types_arg_parser.get_str(value))

        self._kwargs["select"] = ",".join(select)

    @property
    def preferred_country_code(self) -> "OptCountryCode":
        return self._kwargs.get("boost")

    @preferred_country_code.setter
    def preferred_country_code(self, value: "OptCountryCode"):
        if value:
            value = f"RCSExchangeCountry eq '{country_code_arg_parser.get_str(value)}'"
            self._kwargs["boost"] = value

    @property
    def _filter(self) -> str:
        return self._kwargs.get("filter")

    def _update_filter(self):
        self._kwargs["filter"] = _prepare_filter(self.asset_state, self.asset_class)

    @property
    def asset_state(self) -> "OptAssetState":
        return self._kwargs.get("asset_state")

    @asset_state.setter
    def asset_state(self, value: "OptAssetState"):
        if value:
            self._kwargs["asset_state"] = asset_state_enum_arg_parser.get_enum(value)
            self._update_filter()

    @property
    def asset_class(self) -> "OptAssetClass":
        return self._kwargs.get("asset_class")

    @asset_class.setter
    def asset_class(self, value: "OptAssetClass"):
        if value:
            value = Copier.get_list(value)
            self._kwargs["asset_class"] = asset_class_enum_arg_parser.get_enum(value)
            self._update_filter()

    @property
    def extended_params(self) -> "ExtendedParams":
        return self._kwargs.get("extended_params")

    @extended_params.setter
    def extended_params(self, value: "ExtendedParams"):
        if value:
            self._kwargs["extended_params"] = value

    def __repr__(self):
        return create_repr(
            self,
            middle_path="content.symbols_convention",
            content=f"{{symbols='{self.symbols}'}}",
        )
