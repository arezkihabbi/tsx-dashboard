from ..._param_item import param_item
from ..._serializable import Serializable


class StrikeFilter(Serializable):
    def __init__(self, max_of_median_implied_vol=None, min_of_median_implied_vol=None):
        super().__init__()
        self.max_of_median_implied_vol = max_of_median_implied_vol
        self.min_of_median_implied_vol = min_of_median_implied_vol

    def _get_items(self):
        return [
            param_item.to_kv("maxOfMedianImpliedVol", self.max_of_median_implied_vol),
            param_item.to_kv("minOfMedianImpliedVol", self.min_of_median_implied_vol),
        ]
