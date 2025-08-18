from enum import unique
from typing import Union, List, Optional

from ..._base_enum import StrEnum
from ..._tools import make_enum_arg_parser_by_members


@unique
class SymbolTypes(StrEnum):
    """
    Symbol types to send in request, by default "RIC" is using.
    """

    RIC = "RIC"
    ISIN = "IssueISIN"
    CUSIP = "CUSIP"
    SEDOL = "SEDOL"
    TICKER_SYMBOL = "TickerSymbol"
    OA_PERM_ID = "IssuerOAPermID"
    LIPPER_ID = "FundClassLipperID"


SYMBOL_TYPE_VALUES = tuple(t for t in SymbolTypes)

SymbolTypesType = Union[str, List[str], SymbolTypes, List[SymbolTypes]]
OptSymbolTypes = Optional[SymbolTypesType]

symbol_types_arg_parser = make_enum_arg_parser_by_members(SymbolTypes)
