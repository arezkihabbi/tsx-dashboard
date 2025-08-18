from typing import Optional, Union

from ._underlying_type import UnderlyingType
from ..eti_option import (
    EtiBarrierDefinition,
    EtiBinaryDefinition,
    EtiCbbcDefinition,
    EtiDoubleBarriersDefinition,
    EtiFixingInfo,
    EtiUnderlyingDefinition,
)
from ..._enums import BuySell, CallPut, ExerciseStyle
from ..._param_item import datetime_param_item, enum_param_item, param_item, serializable_param_item
from ..._serializable import Serializable
from ....._types import OptDateTime


class EtiDefinition(Serializable):
    def __init__(
        self,
        instrument_tag: Optional[str] = None,
        instrument_code: Optional[str] = None,
        start_date: "OptDateTime" = None,
        end_date: "OptDateTime" = None,
        asian_definition: Optional[EtiFixingInfo] = None,
        barrier_definition: Optional[EtiBarrierDefinition] = None,
        binary_definition: Optional[EtiBinaryDefinition] = None,
        buy_sell: Union[BuySell, str] = None,
        call_put: Union[CallPut, str] = None,
        cbbc_definition: Optional[EtiCbbcDefinition] = None,
        double_barriers_definition: Optional[EtiDoubleBarriersDefinition] = None,
        exercise_style: Union[ExerciseStyle, str] = None,
        underlying_definition: Optional[EtiUnderlyingDefinition] = None,
        underlying_type: Union[UnderlyingType, str] = None,
        deal_contract: Optional[int] = None,
        end_date_time: "OptDateTime" = None,
        lot_size: Optional[float] = None,
        strike: Optional[float] = None,
        time_zone_offset: Optional[int] = None,
    ) -> None:
        super().__init__()
        self.instrument_tag = instrument_tag
        self.instrument_code = instrument_code
        self.start_date = start_date
        self.end_date = end_date
        self.asian_definition = asian_definition
        self.barrier_definition = barrier_definition
        self.binary_definition = binary_definition
        self.buy_sell = buy_sell
        self.call_put = call_put
        self.cbbc_definition = cbbc_definition
        self.double_barriers_definition = double_barriers_definition
        self.exercise_style = exercise_style
        self.underlying_definition = underlying_definition
        self.underlying_type = underlying_type
        self.deal_contract = deal_contract
        self.end_date_time = end_date_time
        self.lot_size = lot_size
        self.strike = strike
        self.time_zone_offset = time_zone_offset

    def _get_items(self):
        return [
            serializable_param_item.to_kv("asianDefinition", self.asian_definition),
            serializable_param_item.to_kv("barrierDefinition", self.barrier_definition),
            serializable_param_item.to_kv("binaryDefinition", self.binary_definition),
            enum_param_item.to_kv("buySell", self.buy_sell),
            enum_param_item.to_kv("callPut", self.call_put),
            serializable_param_item.to_kv("cbbcDefinition", self.cbbc_definition),
            serializable_param_item.to_kv("doubleBarriersDefinition", self.double_barriers_definition),
            enum_param_item.to_kv("exerciseStyle", self.exercise_style),
            serializable_param_item.to_kv("underlyingDefinition", self.underlying_definition),
            enum_param_item.to_kv("underlyingType", self.underlying_type),
            param_item.to_kv("dealContract", self.deal_contract),
            datetime_param_item.to_kv("endDate", self.end_date),
            datetime_param_item.to_kv("endDateTime", self.end_date_time),
            param_item.to_kv("instrumentCode", self.instrument_code),
            param_item.to_kv("instrumentTag", self.instrument_tag),
            param_item.to_kv("lotSize", self.lot_size),
            datetime_param_item.to_kv("startDate", self.start_date),
            param_item.to_kv("strike", self.strike),
            param_item.to_kv("timeZoneOffset", self.time_zone_offset),
        ]
