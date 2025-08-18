from ..._param_item import param_item
from ..._serializable import Serializable
from ....._types import OptInt, OptFloat


class Turn(Serializable):
    """
    Parameters
    ----------
    month : int, optional
        Month of the turn period
    rate_percent : float, optional
        Turn rate expressed in percents
    year : int, optional
        Year of the turn period
    """

    def __init__(
        self,
        month: OptInt = None,
        rate_percent: OptFloat = None,
        year: OptInt = None,
    ) -> None:
        super().__init__()
        self.month = month
        self.rate_percent = rate_percent
        self.year = year

    def _get_items(self):
        return [
            param_item.to_kv("month", self.month),
            param_item.to_kv("ratePercent", self.rate_percent),
            param_item.to_kv("year", self.year),
        ]
