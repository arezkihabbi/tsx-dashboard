from ..._curves._cross_currency_curves import MainConstituentAssetClass, RiskType
from ....._tools import EnumArgsParser, make_parse_enum, make_convert_to_enum


main_constituent_asset_class_arg_parser = EnumArgsParser(
    parse=make_parse_enum(MainConstituentAssetClass),
    parse_to_enum=make_convert_to_enum(MainConstituentAssetClass),
)

risk_type_arg_parser = EnumArgsParser(
    parse=make_parse_enum(RiskType),
    parse_to_enum=make_convert_to_enum(RiskType),
)
