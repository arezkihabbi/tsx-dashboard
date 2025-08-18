from typing import Optional, Union

from ..._enums import BarrierMode, InOrOut, UpOrDown
from ..._param_item import param_item, enum_param_item, datetime_param_item
from ..._serializable import Serializable


class FxBarrierDefinition(Serializable):
    """
    Parameters
    ----------
    barrier_mode : BarrierMode or str, optional
        Barrier Mode of the barrier option
    in_or_out : InOrOut or str, optional
        In/Out property of the barrier option
    up_or_down : UpOrDown or str, optional
        Up/Down property of the barrier option
    level : float, optional
        Barrier of the barrier option
    rebate_amount : float, optional
        Rebate of the barrier option
    window_end_date : str or date or datetime or timedelta, optional
        Window Start date of the barrier option
    window_start_date : str or date or datetime or timedelta, optional
        Window Start date of the barrier option
    """

    def __init__(
        self,
        barrier_mode: Union[BarrierMode, str] = None,
        in_or_out: Union[InOrOut, str] = None,
        up_or_down: Union[UpOrDown, str] = None,
        level: Optional[float] = None,
        rebate_amount: Optional[float] = None,
        window_end_date: "OptDateTime" = None,
        window_start_date: "OptDateTime" = None,
    ) -> None:
        super().__init__()
        self.barrier_mode = barrier_mode
        self.in_or_out = in_or_out
        self.up_or_down = up_or_down
        self.level = level
        self.rebate_amount = rebate_amount
        self.window_end_date = window_end_date
        self.window_start_date = window_start_date

    def _get_items(self):
        return [
            enum_param_item.to_kv("barrierMode", self.barrier_mode),
            enum_param_item.to_kv("inOrOut", self.in_or_out),
            enum_param_item.to_kv("upOrDown", self.up_or_down),
            param_item.to_kv("level", self.level),
            param_item.to_kv("rebateAmount", self.rebate_amount),
            datetime_param_item.to_kv("windowEndDate", self.window_end_date),
            datetime_param_item.to_kv("windowStartDate", self.window_start_date),
        ]
