from typing import TYPE_CHECKING

from ..._param_item import param_item
from ..._serializable import Serializable

if TYPE_CHECKING:
    from ....._types import OptStr, OptFloat


class MaturityFilter(Serializable):
    """
    MaturityFilter for surface.

    Parameters
    ----------
    max_maturity : str, optional
        The period code used to set the maximal maturity of options used to construct
        the surface (e.g., '1M', '1Y').
    min_maturity : str, optional
        The period code used to set the minimal maturity of options used to construct
        the surface (e.g., '1M', '1Y').
    min_of_median_nb_of_strikes_percent : float, optional
        The value is used to set the minimum number of strikes that should be available
        for maturities that are used to construct the surface. The minimum threshold
        is computed as MinOfMedianNbOfStrikesPercent multiplied by the median number
        of Strikes and divided by 100. The value is expressed in percentages.
    """

    def __init__(
        self,
        max_maturity: "OptStr" = None,
        min_maturity: "OptStr" = None,
        min_of_median_nb_of_strikes_percent: "OptFloat" = None,
    ):
        super().__init__()
        self.max_maturity = max_maturity
        self.min_maturity = min_maturity
        self.min_of_median_nb_of_strikes_percent = min_of_median_nb_of_strikes_percent

    def _get_items(self):
        return [
            param_item.to_kv("maxMaturity", self.max_maturity),
            param_item.to_kv("minMaturity", self.min_maturity),
            param_item.to_kv("minOfMedianNbOfStrikesPercent", self.min_of_median_nb_of_strikes_percent),
        ]
