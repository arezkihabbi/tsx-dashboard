from typing import Optional, Union

from ..._enums import InOrOut
from ..._param_item import param_item
from ..._serializable import Serializable


class FxDoubleBarrierInfo(Serializable):
    def __init__(
        self,
        in_or_out: Union[InOrOut, str] = None,
        level: Optional[float] = None,
        rebate_amount: Optional[float] = None,
    ):
        super().__init__()
        self.in_or_out = in_or_out
        self.level = level
        self.rebate_amount = rebate_amount

    def _get_items(self):
        return [
            param_item.to_kv("inOrOut", self.in_or_out),
            param_item.to_kv("level", self.level),
            param_item.to_kv("rebateAmount", self.rebate_amount),
        ]
