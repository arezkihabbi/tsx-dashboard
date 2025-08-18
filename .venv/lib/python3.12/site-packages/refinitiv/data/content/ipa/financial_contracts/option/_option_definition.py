from typing import Optional, Union

from ._underlying_type import UnderlyingType
from ..._enums import BuySell, CallPut, ExerciseStyle
from ..._param_item import datetime_param_item, enum_param_item, param_item
from ..._serializable import Serializable
from ....._types import OptDateTime


class OptionDefinition(Serializable):
    def __init__(
        self,
        instrument_tag: Optional[str] = None,
        start_date: "OptDateTime" = None,
        end_date: "OptDateTime" = None,
        buy_sell: Union[BuySell, str] = None,
        call_put: Union[CallPut, str] = None,
        exercise_style: Union[ExerciseStyle, str] = None,
        underlying_type: Union[UnderlyingType, str] = None,
        strike: Optional[float] = None,
    ) -> None:
        super().__init__()
        self.instrument_tag = instrument_tag
        self.start_date = start_date
        self.end_date = end_date
        self.buy_sell = buy_sell
        self.call_put = call_put
        self.exercise_style = exercise_style
        self.underlying_type = underlying_type
        self.strike = strike

    @staticmethod
    def get_instrument_type():
        return "Option"

    def _get_items(self):
        return [
            enum_param_item.to_kv("buySell", self.buy_sell),
            enum_param_item.to_kv("callPut", self.call_put),
            enum_param_item.to_kv("exerciseStyle", self.exercise_style),
            enum_param_item.to_kv("underlyingType", self.underlying_type),
            datetime_param_item.to_kv("endDate", self.end_date),
            datetime_param_item.to_kv("startDate", self.start_date),
            param_item.to_kv("strike", self.strike),
            param_item.to_kv("instrumentTag", self.instrument_tag),
        ]
