from typing import Optional

from .._enums import BarrierType
from .._param_item import enum_param_item, param_item
from .._serializable import Serializable


class BarrierDefinitionElement(Serializable):
    def __init__(
        self,
        barrier_type: Optional[BarrierType] = None,
        barrier_down_percent: Optional[float] = None,
        barrier_up_percent: Optional[float] = None,
        rebate_down_percent: Optional[float] = None,
        rebate_up_percent: Optional[float] = None,
    ):
        super().__init__()
        self.barrier_type = barrier_type
        self.barrier_down_percent = barrier_down_percent
        self.barrier_up_percent = barrier_up_percent
        self.rebate_down_percent = rebate_down_percent
        self.rebate_up_percent = rebate_up_percent

    def _get_items(self):
        return [
            enum_param_item.to_kv("barrierType", self.barrier_type),
            param_item.to_kv("barrierDownPercent", self.barrier_down_percent),
            param_item.to_kv("barrierUpPercent", self.barrier_up_percent),
            param_item.to_kv("rebateDownPercent", self.rebate_down_percent),
            param_item.to_kv("rebateUpPercent", self.rebate_up_percent),
        ]
