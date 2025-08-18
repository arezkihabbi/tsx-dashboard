from typing import Optional, List, Union, TYPE_CHECKING

from ._average_info import FxAverageInfo
from ._barrier_definition import FxBarrierDefinition
from ._binary_definition import FxBinaryDefinition
from ._double_barrier_definition import FxDoubleBarrierDefinition
from ._double_binary_definition import FxDoubleBinaryDefinition
from ._dual_currency_definition import FxDualCurrencyDefinition
from ._forward_start import FxForwardStart
from ._underlying_definition import FxUnderlyingDefinition
from ..._enums import BuySell, CallPut, ExerciseStyle, UnderlyingType, SettlementType
from ..._models import InputFlow
from ..._param_item import (
    param_item,
    enum_param_item,
    list_serializable_param_item,
    serializable_param_item,
    datetime_param_item,
)
from ..._serializable import Serializable

if TYPE_CHECKING:
    from ....._types import OptDateTime


class FxDefinition(Serializable):
    def __init__(
        self,
        instrument_tag: Optional[str] = None,
        start_date: "OptDateTime" = None,
        end_date: "OptDateTime" = None,
        tenor: Optional[str] = None,
        notional_ccy: Optional[str] = None,
        notional_amount: Optional[float] = None,
        asian_definition: Optional[FxAverageInfo] = None,
        barrier_definition: Optional[FxBarrierDefinition] = None,
        binary_definition: Optional[FxBinaryDefinition] = None,
        buy_sell: Union[BuySell, str] = None,
        call_put: Union[CallPut, str] = None,
        double_barrier_definition: Optional[FxDoubleBarrierDefinition] = None,
        double_binary_definition: Optional[FxDoubleBinaryDefinition] = None,
        dual_currency_definition: Optional[FxDualCurrencyDefinition] = None,
        exercise_style: Union[ExerciseStyle, str] = None,
        forward_start_definition: Optional[FxForwardStart] = None,
        payments: Optional[List[InputFlow]] = None,
        settlement_type: Union[SettlementType, str] = None,
        underlying_definition: Optional[FxUnderlyingDefinition] = None,
        underlying_type: Union[UnderlyingType, str] = None,
        delivery_date: "OptDateTime" = None,
        settlement_ccy: Optional[str] = None,
        strike: Optional[float] = None,
    ) -> None:
        super().__init__()
        self.instrument_tag = instrument_tag
        self.start_date = start_date
        self.end_date = end_date
        self.tenor = tenor
        self.notional_ccy = notional_ccy
        self.notional_amount = notional_amount
        self.asian_definition = asian_definition
        self.barrier_definition = barrier_definition
        self.binary_definition = binary_definition
        self.buy_sell = buy_sell
        self.call_put = call_put
        self.double_barrier_definition = double_barrier_definition
        self.double_binary_definition = double_binary_definition
        self.dual_currency_definition = dual_currency_definition
        self.exercise_style = exercise_style
        self.forward_start_definition = forward_start_definition
        self.payments = payments
        self.settlement_type = settlement_type
        self.underlying_definition = underlying_definition
        self.underlying_type = underlying_type
        self.delivery_date = delivery_date
        self.settlement_ccy = settlement_ccy
        self.strike = strike

    @staticmethod
    def get_instrument_type():
        return "Option"

    def _get_items(self):
        return [
            serializable_param_item.to_kv("asianDefinition", self.asian_definition),
            serializable_param_item.to_kv("barrierDefinition", self.barrier_definition),
            serializable_param_item.to_kv("binaryDefinition", self.binary_definition),
            enum_param_item.to_kv("buySell", self.buy_sell),
            enum_param_item.to_kv("callPut", self.call_put),
            serializable_param_item.to_kv("doubleBarrierDefinition", self.double_barrier_definition),
            serializable_param_item.to_kv("doubleBinaryDefinition", self.double_binary_definition),
            serializable_param_item.to_kv("dualCurrencyDefinition", self.dual_currency_definition),
            enum_param_item.to_kv("exerciseStyle", self.exercise_style),
            serializable_param_item.to_kv("forwardStartDefinition", self.forward_start_definition),
            list_serializable_param_item.to_kv("payments", self.payments),
            enum_param_item.to_kv("settlementType", self.settlement_type),
            serializable_param_item.to_kv("underlyingDefinition", self.underlying_definition),
            enum_param_item.to_kv("underlyingType", self.underlying_type),
            datetime_param_item.to_kv("deliveryDate", self.delivery_date),
            datetime_param_item.to_kv("endDate", self.end_date),
            param_item.to_kv("instrumentTag", self.instrument_tag),
            param_item.to_kv("notionalAmount", self.notional_amount),
            param_item.to_kv("notionalCcy", self.notional_ccy),
            param_item.to_kv("settlementCcy", self.settlement_ccy),
            datetime_param_item.to_kv("startDate", self.start_date),
            param_item.to_kv("strike", self.strike),
            param_item.to_kv("tenor", self.tenor),
        ]
