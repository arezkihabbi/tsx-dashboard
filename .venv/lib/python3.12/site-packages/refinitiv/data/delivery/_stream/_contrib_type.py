from enum import Enum
from typing import Union

from ..._tools import EnumArgsParser, make_parse_enum, make_convert_to_enum


class ContribType(Enum):
    REFRESH = "Refresh"
    UPDATE = "Update"


OptContribT = Union[str, ContribType, None]

contrib_type_enum_arg_parser = EnumArgsParser(
    parse=make_parse_enum(ContribType),
    parse_to_enum=make_convert_to_enum(ContribType),
)
