from typing import TYPE_CHECKING, Union

from .. import content
from ..content.symbol_conversion._definition import DEFAULT_SCOPE
from ..content.symbol_conversion._symbol_type import SYMBOL_TYPE_VALUES

if TYPE_CHECKING:
    from ..content.symbol_conversion._symbol_type import SymbolTypesType
    from ..content.symbol_conversion._symbol_type import SymbolTypes
    from .._types import StrStrings
    from ..content.symbol_conversion._asset_class import OptAssetClass
    from ..content.symbol_conversion._asset_state import OptAssetState
    from ..content.symbol_conversion._country_code import OptCountryCode


def convert_symbols(
    symbols: "StrStrings",
    from_symbol_type: Union[str, "SymbolTypes"] = DEFAULT_SCOPE,
    to_symbol_types: "SymbolTypesType" = SYMBOL_TYPE_VALUES,
    preferred_country_code: "OptCountryCode" = None,
    asset_class: "OptAssetClass" = None,
    asset_state: "OptAssetState" = None,
):
    """
    This function describes parameters to convert symbols

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

    preferred_country_code: str or CountryCode, optional
        Unique ISO 3166 code for country

    asset_class: str or AssetClass, optional
        AssetClass value to build filter parameter.

    asset_state: str or AssetState, optional
        AssetState value to build filter parameter.

    Returns
    -------
    pd.DataFrame

    Examples
    --------
    >>> import refinitiv.data as rd
    >>> df = rd.discovery.convert_symbols(symbols=["US5949181045", "US02079K1079"], to_symbol_types="RIC")

    """
    return (
        content.symbol_conversion.Definition(
            symbols=symbols,
            from_symbol_type=from_symbol_type,
            to_symbol_types=to_symbol_types,
            preferred_country_code=preferred_country_code,
            asset_class=asset_class,
            asset_state=asset_state,
        )
        .get_data()
        .data.df
    )
