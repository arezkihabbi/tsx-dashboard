from typing import Optional, TYPE_CHECKING, List

from ._swap_definition import SwapInstrumentDefinition
from .._base_financial_contracts_definition import BaseFinancialContractsDefinition
from ...._content_provider_layer import PosArgsWarnMixin
from ....._tools import try_copy_to_list

if TYPE_CHECKING:
    from ....._types import ExtendedParams, OptStrStrs, OptDateTime
    from . import LegDefinition, PricingParameters


class Definition(BaseFinancialContractsDefinition, PosArgsWarnMixin):
    _WARN_NAME = "financial_contracts.swap.Definition"
    _WARN_EX = "use financial_contracts.swap.Definition(instrument_tag='user-defined GBP IRS') instead of financial_contracts.swap.Definition('user-defined GBP IRS')"

    def __init__(
        self,
        instrument_tag: Optional[str] = None,
        instrument_code: Optional[str] = None,
        trade_date: "OptDateTime" = None,
        start_date: "OptDateTime" = None,
        end_date: "OptDateTime" = None,
        tenor: Optional[str] = None,
        legs: Optional[List["LegDefinition"]] = None,
        is_non_deliverable: Optional[bool] = None,
        settlement_ccy: Optional[str] = None,
        start_tenor: Optional[str] = None,
        template: Optional[str] = None,
        fields: "OptStrStrs" = None,
        pricing_parameters: Optional["PricingParameters"] = None,
        extended_params: "ExtendedParams" = None,
    ):
        legs = try_copy_to_list(legs)
        fields = try_copy_to_list(fields)
        definition = SwapInstrumentDefinition(
            legs=legs,
            end_date=end_date,
            instrument_code=instrument_code,
            instrument_tag=instrument_tag,
            is_non_deliverable=is_non_deliverable,
            settlement_ccy=settlement_ccy,
            start_date=start_date,
            start_tenor=start_tenor,
            template=template,
            tenor=tenor,
            trade_date=trade_date,
        )
        super().__init__(
            definition=definition,
            fields=fields,
            pricing_parameters=pricing_parameters,
            extended_params=extended_params,
        )
