from typing import Optional, Union

from ..._enums import BarrierStyle, InOrOut, UpOrDown
from ..._param_item import param_item, enum_param_item
from ..._serializable import Serializable


class EtiBarrierDefinition(Serializable):
    """
    Parameters
    ----------
    barrier_style : BarrierStyle or str, optional

    in_or_out : InOrOut or str, optional

    up_or_down : UpOrDown or str, optional

    level : float, optional

    """

    def __init__(
        self,
        barrier_style: Union[BarrierStyle, str] = None,
        in_or_out: Union[InOrOut, str] = None,
        up_or_down: Union[UpOrDown, str] = None,
        level: Optional[float] = None,
    ) -> None:
        super().__init__()
        self.barrier_style = barrier_style
        self.in_or_out = in_or_out
        self.up_or_down = up_or_down
        self.level = level

    def _get_items(self):
        return [
            enum_param_item.to_kv("barrierStyle", self.barrier_style),
            enum_param_item.to_kv("inOrOut", self.in_or_out),
            enum_param_item.to_kv("upOrDown", self.up_or_down),
            param_item.to_kv("level", self.level),
        ]
