from typing import Optional

from ..._param_item import param_item, datetime_param_item
from ..._serializable import Serializable
from ....._types import OptDateTime


class FxForwardStart(Serializable):
    """
    Parameters
    ----------
    forward_start_date : str or date or datetime or timedelta, optional
        Expiry date of the Forward Start option
    forward_start_tenor : str, optional
        Tenor of the Forward Start option
    strike_percent : float, optional
        Strike Percent of the Forward Start date of the option
    """

    def __init__(
        self,
        forward_start_date: "OptDateTime" = None,
        forward_start_tenor: Optional[str] = None,
        strike_percent: Optional[float] = None,
    ) -> None:
        super().__init__()
        self.forward_start_date = forward_start_date
        self.forward_start_tenor = forward_start_tenor
        self.strike_percent = strike_percent

    def _get_items(self):
        return [
            datetime_param_item.to_kv("forwardStartDate", self.forward_start_date),
            param_item.to_kv("forwardStartTenor", self.forward_start_tenor),
            param_item.to_kv("strikePercent", self.strike_percent),
        ]
