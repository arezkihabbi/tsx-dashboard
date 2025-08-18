from typing import Optional, List, Union

from . import BermudanSwaptionDefinition
from .. import swap
from ..._enums import BuySell, ExerciseStyle, PremiumSettlementType, SwaptionSettlementType, SwaptionType
from ..._models import InputFlow
from ..._param_item import (
    param_item,
    datetime_param_item,
    serializable_param_item,
    enum_param_item,
    list_serializable_param_item,
    definition_param_item,
)
from ..._serializable import Serializable
from ....._types import OptDateTime


class SwaptionInstrumentDefinition(Serializable):
    def __init__(
        self,
        instrument_tag: Optional[str] = None,
        start_date: "OptDateTime" = None,
        end_date: "OptDateTime" = None,
        tenor: Optional[str] = None,
        notional_amount: Optional[float] = None,
        bermudan_swaption_definition: Optional[BermudanSwaptionDefinition] = None,
        buy_sell: Union[BuySell, str] = None,
        exercise_style: Union[ExerciseStyle, str] = None,
        payments: Optional[List[InputFlow]] = None,
        premium_settlement_type: Union[PremiumSettlementType, str] = None,
        settlement_type: Union[SwaptionSettlementType, str] = None,
        swaption_type: Union[SwaptionType, str] = None,
        underlying_definition: Optional[swap.Definition] = None,
        spread_vs_atm_in_bp: Optional[float] = None,
        strike_percent: Optional[float] = None,
        delivery_date: "OptDateTime" = None,
    ) -> None:
        super().__init__()
        self.instrument_tag = instrument_tag
        self.start_date = start_date
        self.end_date = end_date
        self.tenor = tenor
        self.notional_amount = notional_amount
        self.bermudan_swaption_definition = bermudan_swaption_definition
        self.buy_sell = buy_sell
        self.exercise_style = exercise_style
        self.payments = payments
        self.premium_settlement_type = premium_settlement_type
        self.settlement_type = settlement_type
        self.swaption_type = swaption_type
        self.underlying_definition = underlying_definition
        self.spread_vs_atm_in_bp = spread_vs_atm_in_bp
        self.strike_percent = strike_percent
        self.delivery_date = delivery_date

    @staticmethod
    def get_instrument_type():
        return "Swaption"

    def _get_items(self):
        return [
            serializable_param_item.to_kv("bermudanSwaptionDefinition", self.bermudan_swaption_definition),
            enum_param_item.to_kv("buySell", self.buy_sell),
            enum_param_item.to_kv("exerciseStyle", self.exercise_style),
            list_serializable_param_item.to_kv("payments", self.payments),
            enum_param_item.to_kv("premiumSettlementType", self.premium_settlement_type),
            enum_param_item.to_kv("settlementType", self.settlement_type),
            enum_param_item.to_kv("swaptionType", self.swaption_type),
            definition_param_item.to_kv("underlyingDefinition", self.underlying_definition),
            datetime_param_item.to_kv("endDate", self.end_date),
            param_item.to_kv("instrumentTag", self.instrument_tag),
            param_item.to_kv("notionalAmount", self.notional_amount),
            param_item.to_kv("spreadVsAtmInBp", self.spread_vs_atm_in_bp),
            datetime_param_item.to_kv("startDate", self.start_date),
            param_item.to_kv("strikePercent", self.strike_percent),
            param_item.to_kv("tenor", self.tenor),
            datetime_param_item.to_kv("deliveryDate", self.delivery_date),
        ]
