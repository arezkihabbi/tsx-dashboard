from typing import TYPE_CHECKING

from ..._param_item import param_item
from ..._serializable import Serializable

if TYPE_CHECKING:
    from ....._types import OptStr


class VolatilitySurfacePoint(Serializable):
    """
    VolatilitySurfacePoint for surface.

    Parameters
    ----------
    x : str, optional
        The coordinate of the volatility data point on the x-axis
    y : str, optional
        The coordinate of the volatility data point on the y-axis
    """

    def __init__(self, x: "OptStr" = None, y: "OptStr" = None):
        super().__init__()
        self.x = x
        self.y = y

    def _get_items(self):
        return [
            param_item.to_kv("x", self.x),
            param_item.to_kv("y", self.y),
        ]
