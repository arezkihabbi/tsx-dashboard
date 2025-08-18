from typing import Optional

from ._swap_leg_definition import LegDefinition
from ..._param_item import list_serializable_param_item, datetime_param_item, param_item
from ..._serializable import Serializable
from ....._types import OptDateTime


class SwapInstrumentDefinition(Serializable):
    def __init__(
        self,
        instrument_tag: Optional[str] = None,
        instrument_code: Optional[str] = None,
        trade_date: "OptDateTime" = None,
        start_date: "OptDateTime" = None,
        end_date: "OptDateTime" = None,
        tenor: Optional[str] = None,
        legs: Optional[LegDefinition] = None,
        is_non_deliverable: Optional[bool] = None,
        settlement_ccy: Optional[str] = None,
        start_tenor: Optional[str] = None,
        template: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.instrument_tag = instrument_tag
        self.instrument_code = instrument_code
        self.trade_date = trade_date
        self.start_date = start_date
        self.end_date = end_date
        self.tenor = tenor
        self.legs = legs
        self.is_non_deliverable = is_non_deliverable
        self.settlement_ccy = settlement_ccy
        self.start_tenor = start_tenor
        self.template = template

    @staticmethod
    def get_instrument_type():
        return "Swap"

    def _get_items(self):
        return [
            list_serializable_param_item.to_kv("legs", self.legs),
            datetime_param_item.to_kv("endDate", self.end_date),
            param_item.to_kv("instrumentCode", self.instrument_code),
            param_item.to_kv("isNonDeliverable", self.is_non_deliverable),
            param_item.to_kv("settlementCcy", self.settlement_ccy),
            datetime_param_item.to_kv("startDate", self.start_date),
            param_item.to_kv("startTenor", self.start_tenor),
            param_item.to_kv("template", self.template),
            param_item.to_kv("tenor", self.tenor),
            datetime_param_item.to_kv("tradeDate", self.trade_date),
            param_item.to_kv("instrumentTag", self.instrument_tag),
        ]
