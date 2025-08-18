from enum import unique
from typing import Union, List, Optional, Iterable

from ..._tools import make_convert_to_enum, EnumArgsParser, make_parse_enum
from ..._base_enum import StrEnum


@unique
class AssetClass(StrEnum):
    """
    Asset class values to build 'filter' parameter in request for SymbolConversion content object.
    """

    COMMODITIES = "Commodities"
    EQUITY_OR_INDEX_OPTIONS = "EquityOrIndexOptions"
    BOND_AND_STIR_FUTURES_AND_OPTIONS = "BondAndSTIRFuturesAndOptions"
    WARRANTS = "Warrants"
    EQUITIES = "Equities"
    INDICES = "Indices"
    EQUITY_INDEX_FUTURES = "EquityIndexFutures"
    FUNDS = "Funds"
    CERTIFICATES = "Certificates"
    BONDS = "Bonds"
    RESERVE_CONVERTIBLE = "ReverseConvertible"
    MINI_FUTURE = "MiniFuture"
    FX_AND_MONEY = "FXAndMoney"


OptAssetClass = Optional[Union[str, List[str], AssetClass, List[AssetClass]]]

asset_class_enum_arg_parser = EnumArgsParser(
    parse=make_parse_enum(AssetClass), parse_to_enum=make_convert_to_enum(AssetClass)
)

search_all_category_by_asset_class = {
    AssetClass.COMMODITIES: "Commodities",
    AssetClass.EQUITY_OR_INDEX_OPTIONS: "Options",
    AssetClass.BOND_AND_STIR_FUTURES_AND_OPTIONS: "Exchange-Traded Rates",
    AssetClass.EQUITIES: "Equities",
    AssetClass.EQUITY_INDEX_FUTURES: "Futures",
    AssetClass.FUNDS: "Funds",
    AssetClass.BONDS: "Bond Pricing",
    AssetClass.FX_AND_MONEY: "FX & Money",
}

rcsasset_category_genealogy_by_asset_class = {
    AssetClass.WARRANTS: "A:AA",
    AssetClass.CERTIFICATES: "A:6N",
    AssetClass.INDICES: "I:17",
    AssetClass.RESERVE_CONVERTIBLE: "A:LE",
    AssetClass.MINI_FUTURE: "A:P6",
}


def _transform_to_string(values: Iterable, category: dict) -> str:
    return " ".join(f"'{category[value]}'" for value in values)


def create_asset_class_request_strings(asset_class: list) -> tuple:
    search_all_category_values = filter(lambda x: x in search_all_category_by_asset_class, asset_class)
    rcs_asset_category_values = filter(lambda x: x in rcsasset_category_genealogy_by_asset_class, asset_class)

    search_all_category_string_values = _transform_to_string(
        search_all_category_values, search_all_category_by_asset_class
    )

    search_all_rcs_asset_category_string_values = _transform_to_string(
        rcs_asset_category_values, rcsasset_category_genealogy_by_asset_class
    )

    search_all_category_string = ""
    rcs_asset_category_string = ""

    if search_all_category_string_values:
        search_all_category_string = f"SearchAllCategoryv3 in ({search_all_category_string_values})"

    if search_all_rcs_asset_category_string_values:
        rcs_asset_category_string = f"RCSAssetCategoryGenealogy in ({search_all_rcs_asset_category_string_values})"

    return search_all_category_string, rcs_asset_category_string
