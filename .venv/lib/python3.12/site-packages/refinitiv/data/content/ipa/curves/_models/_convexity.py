from ..._param_item import param_item
from ..._serializable import Serializable
from ....._types import OptFloat


class ConvexityAdjustment(Serializable):
    """
    Parameters
    ----------
    mean_reversion_percent : float, optional
        Reversion speed rate, expressed in percents, used to calculate the convexity
        adjustment
    volatility_percent : float, optional
        Reversion flat volatility, expressed in percents, used to calculate the
        convexity adjustment
    """

    def __init__(
        self,
        mean_reversion_percent: OptFloat = None,
        volatility_percent: OptFloat = None,
    ) -> None:
        super().__init__()
        self.mean_reversion_percent = mean_reversion_percent
        self.volatility_percent = volatility_percent

    def _get_items(self):
        return [
            param_item.to_kv("meanReversionPercent", self.mean_reversion_percent),
            param_item.to_kv("volatilityPercent", self.volatility_percent),
        ]
