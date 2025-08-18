from typing import Optional

from ._eti_definition import EtiDefinition
from ._option_definition import OptionDefinition
from ._underlying_type import UnderlyingType
from ..eti_option import (
    EtiUnderlyingDefinition,
    EtiBinaryDefinition,
    EtiBarrierDefinition,
    EtiCbbcDefinition,
    EtiDoubleBarriersDefinition,
    EtiFixingInfo,
)
from ..fx_option import FxDualCurrencyDefinition, FxDoubleBarrierDefinition, FxDoubleBinaryDefinition, FxForwardStart
from ..fx_option._fx_definition import FxDefinition
from ..._enums import BuySell, CallPut, ExerciseStyle, SettlementType
from ..._models import InputFlow
from ....._types import OptDateTime


class OptionInstrumentDefinition(EtiDefinition, FxDefinition, OptionDefinition):
    def __init__(
        self,
        asian_definition: Optional[EtiFixingInfo] = None,
        barrier_definition: Optional[EtiBarrierDefinition] = None,
        binary_definition: Optional[EtiBinaryDefinition] = None,
        buy_sell: Optional[BuySell] = None,
        call_put: Optional[CallPut] = None,
        cbbc_definition: Optional[EtiCbbcDefinition] = None,
        deal_contract: Optional[int] = None,
        delivery_date: "OptDateTime" = None,
        double_barrier_definition: Optional[FxDoubleBarrierDefinition] = None,
        double_barriers_definition: Optional[EtiDoubleBarriersDefinition] = None,
        double_binary_definition: Optional[FxDoubleBinaryDefinition] = None,
        dual_currency_definition: Optional[FxDualCurrencyDefinition] = None,
        end_date: "OptDateTime" = None,
        end_date_time: "OptDateTime" = None,
        exercise_style: Optional[ExerciseStyle] = None,
        forward_start_definition: Optional[FxForwardStart] = None,
        instrument_code: Optional[str] = None,
        instrument_tag: Optional[str] = None,
        lot_size: Optional[float] = None,
        notional_amount: Optional[float] = None,
        notional_ccy: Optional[str] = None,
        payments: Optional[InputFlow] = None,
        settlement_ccy: Optional[str] = None,
        settlement_type: Optional[SettlementType] = None,
        start_date: "OptDateTime" = None,
        strike: Optional[float] = None,
        tenor: Optional[str] = None,
        time_zone_offset: Optional[int] = None,
        underlying_definition: Optional[EtiUnderlyingDefinition] = None,
        underlying_type: Optional[UnderlyingType] = None,
    ):
        EtiDefinition.__init__(
            self,
            asian_definition=asian_definition,
            barrier_definition=barrier_definition,
            binary_definition=binary_definition,
            buy_sell=buy_sell,
            call_put=call_put,
            cbbc_definition=cbbc_definition,
            deal_contract=deal_contract,
            double_barriers_definition=double_barriers_definition,
            end_date=end_date,
            end_date_time=end_date_time,
            exercise_style=exercise_style,
            instrument_code=instrument_code,
            instrument_tag=instrument_tag,
            lot_size=lot_size,
            start_date=start_date,
            strike=strike,
            time_zone_offset=time_zone_offset,
            underlying_definition=underlying_definition,
            underlying_type=underlying_type,
        )
        FxDefinition.__init__(
            self,
            asian_definition=asian_definition,
            barrier_definition=barrier_definition,
            binary_definition=binary_definition,
            buy_sell=buy_sell,
            call_put=call_put,
            delivery_date=delivery_date,
            double_barrier_definition=double_barrier_definition,
            double_binary_definition=double_binary_definition,
            dual_currency_definition=dual_currency_definition,
            end_date=end_date,
            exercise_style=exercise_style,
            forward_start_definition=forward_start_definition,
            instrument_tag=instrument_tag,
            notional_amount=notional_amount,
            notional_ccy=notional_ccy,
            payments=payments,
            settlement_ccy=settlement_ccy,
            settlement_type=settlement_type,
            start_date=start_date,
            strike=strike,
            tenor=tenor,
            underlying_definition=underlying_definition,
            underlying_type=underlying_type,
        )
        OptionDefinition.__init__(
            self,
            buy_sell=buy_sell,
            call_put=call_put,
            end_date=end_date,
            exercise_style=exercise_style,
            instrument_tag=instrument_tag,
            start_date=start_date,
            strike=strike,
            underlying_type=underlying_type,
        )

    def _get_items(self):
        return EtiDefinition._get_items(self) + FxDefinition._get_items(self) + OptionDefinition._get_items(self)
