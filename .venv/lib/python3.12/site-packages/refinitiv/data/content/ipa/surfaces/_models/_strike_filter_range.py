from typing import TYPE_CHECKING

from ..._param_item import param_item
from ..._serializable import Serializable

if TYPE_CHECKING:
    from ....._types import OptFloat


class StrikeFilterRange(Serializable):
    """
    StrikeFilterRange for surface.

    Parameters
    ----------
    max_of_median_implied_vol_percent : float, optional
        The value can be used to exclude strikes with implied volatilities larger
        than upper bound. The upper bound is computed as MaxOfMedianImpliedVolPercent
        multiplied by median implied volatility and divided by 100. The value is
        expressed in percentages.
        Mandatory if strikeRange object is used.
    min_of_median_implied_vol_percent : float, optional
        The value can be used to exclude strikes with implied volatilities less than
        lower bound. The lower bound is computed as MinOfMedianImpliedVolPercent
        multiplied by median implied volatility and divided by 100.
        The value is expressed in percentages.
    """

    def __init__(
        self,
        max_of_median_implied_vol_percent: "OptFloat" = None,
        min_of_median_implied_vol_percent: "OptFloat" = None,
    ):
        super().__init__()
        self.max_of_median_implied_vol_percent = max_of_median_implied_vol_percent
        self.min_of_median_implied_vol_percent = min_of_median_implied_vol_percent

    def _get_items(self):
        return [
            param_item.to_kv("maxOfMedianImpliedVolPercent", self.max_of_median_implied_vol_percent),
            param_item.to_kv("minOfMedianImpliedVolPercent", self.min_of_median_implied_vol_percent),
        ]
