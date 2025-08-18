from typing import TYPE_CHECKING

from ..._param_item import param_item
from ..._serializable import Serializable

if TYPE_CHECKING:
    from ....._types import OptStr, OptFloat, OptInt


class FxStatisticsParameters(Serializable):
    """
    FxStatisticsParameters for surface.

    Parameters
    ----------
    high_delta : float, optional

    low_delta : float, optional

    model : str, optional

    nb_points : int, optional
    """

    def __init__(
        self,
        *,
        high_delta: "OptFloat" = None,
        low_delta: "OptFloat" = None,
        model: "OptStr" = None,
        nb_points: "OptInt" = None,
    ) -> None:
        super().__init__()
        self.high_delta = high_delta
        self.low_delta = low_delta
        self.model = model
        self.nb_points = nb_points

    def _get_items(self):
        return [
            param_item.to_kv("highDelta", self.high_delta),
            param_item.to_kv("lowDelta", self.low_delta),
            param_item.to_kv("model", self.model),
            param_item.to_kv("nbPoints", self.nb_points),
        ]
