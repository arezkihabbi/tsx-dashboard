from typing import Optional

from . import ParRateShift
from ..._param_item import param_item, serializable_param_item
from ..._serializable import Serializable


class ShiftScenario(Serializable):
    """
    Parameters
    ----------
    par_rate_shift : ParRateShift, optional
        Scenario of par rates shift (shift applied to constituents).
    shift_tag : str, optional
        User defined string to identify the shift scenario tag. it can be used to link
        output curve to the shift scenario. only alphabetic, numeric and '- _.#=@'
        characters are supported. optional.
    zc_curve_shift : dict, optional
        Collection of shift parameters tenor. "all" selector supported as well.
    """

    def __init__(
        self,
        *,
        par_rate_shift: Optional[ParRateShift] = None,
        shift_tag: Optional[str] = None,
        zc_curve_shift: Optional[dict] = None,
    ) -> None:
        super().__init__()
        self.par_rate_shift = par_rate_shift
        self.shift_tag = shift_tag
        self.zc_curve_shift = zc_curve_shift

    def _get_items(self):
        return [
            serializable_param_item.to_kv("parRateShift", self.par_rate_shift),
            param_item.to_kv("shiftTag", self.shift_tag),
            param_item.to_kv("zcCurveShift", self.zc_curve_shift),
        ]
