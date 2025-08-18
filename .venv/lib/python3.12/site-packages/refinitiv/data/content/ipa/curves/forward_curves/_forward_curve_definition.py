from typing import TYPE_CHECKING

from ..._param_item import param_item, date_param_item
from ..._serializable import Serializable
from ...._content_provider_layer import PosArgsWarnMixin
from ....._tools import try_copy_to_list

if TYPE_CHECKING:
    from ....._types import OptStr, OptStrings, OptDateTime


class ForwardCurveDefinition(Serializable, PosArgsWarnMixin):
    """
    Parameters
    ----------
    index_tenor : str, optional

    forward_curve_tenors : list of str, optional
        Defines expected forward rate surface tenor/slices
    forward_curve_tag : str, optional

    forward_start_date : str or date or datetime or timedelta, optional
        Defines the forward start date by date format
    forward_start_tenor : str, optional
        Defines the forward start date by tenor format: "Spot" / "1M" / ...
    """

    def __init__(
        self,
        index_tenor: "OptStr" = None,
        forward_curve_tag: "OptStr" = None,
        forward_curve_tenors: "OptStrings" = None,
        forward_start_date: "OptDateTime" = None,
        forward_start_tenor: "OptStr" = None,
    ) -> None:
        super().__init__()
        self.index_tenor = index_tenor
        self.forward_curve_tenors = try_copy_to_list(forward_curve_tenors)
        self.forward_curve_tag = forward_curve_tag
        self.forward_start_date = forward_start_date
        self.forward_start_tenor = forward_start_tenor

    def _get_items(self):
        return [
            param_item.to_kv("indexTenor", self.index_tenor),
            param_item.to_kv("forwardCurveTenors", self.forward_curve_tenors),
            param_item.to_kv("forwardCurveTag", self.forward_curve_tag),
            date_param_item.to_kv("forwardStartDate", self.forward_start_date),
            param_item.to_kv("forwardStartTenor", self.forward_start_tenor),
        ]
