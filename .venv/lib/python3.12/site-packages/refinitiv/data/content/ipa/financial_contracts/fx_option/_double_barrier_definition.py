from typing import Optional, Union

from ._double_barrier_info import FxDoubleBarrierInfo
from ..._enums import BarrierMode
from ..._param_item import enum_param_item, serializable_param_item
from ..._serializable import Serializable


class FxDoubleBarrierDefinition(Serializable):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    barrier_down : FxDoubleBarrierInfo, optional
        Barrier Information for the lower barrier
    barrier_mode : BarrierMode or str, optional
        Barrier Mode of the double barrier option
    barrier_up : FxDoubleBarrierInfo, optional
        Barrier Information for the upper barrier
    """

    def __init__(
        self,
        barrier_down: Optional[FxDoubleBarrierInfo] = None,
        barrier_mode: Union[BarrierMode, str] = None,
        barrier_up: Optional[FxDoubleBarrierInfo] = None,
    ) -> None:
        super().__init__()
        self.barrier_down = barrier_down
        self.barrier_mode = barrier_mode
        self.barrier_up = barrier_up

    def _get_items(self):
        return [
            serializable_param_item.to_kv("barrierDown", self.barrier_down),
            enum_param_item.to_kv("barrierMode", self.barrier_mode),
            serializable_param_item.to_kv("barrierUp", self.barrier_up),
        ]
