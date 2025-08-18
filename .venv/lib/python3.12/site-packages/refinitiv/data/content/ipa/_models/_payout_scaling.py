from typing import Optional

from .._param_item import param_item
from .._serializable import Serializable


class PayoutScaling(Serializable):
    """
    Parameters
    ----------
    maximum : float, optional

    minimum : float, optional

    """

    def __init__(
        self,
        maximum: Optional[float] = None,
        minimum: Optional[float] = None,
    ) -> None:
        super().__init__()
        self.maximum = maximum
        self.minimum = minimum

    def _get_items(self):
        return [
            param_item.to_kv("maximum", self.maximum),
            param_item.to_kv("minimum", self.minimum),
        ]
