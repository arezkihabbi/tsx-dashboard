from ..._param_item import param_item
from ..._serializable import Serializable


class FxVolatilitySurfaceDefinition(Serializable):
    """
    The definition of the volatility surface.

    Parameters
    ----------
    fx_cross_code : str
        The currency pair of FX Cross, expressed in ISO 4217 alphabetical format
        (e.g., 'EURCHF').
    """

    def __init__(self, fx_cross_code: str = None):
        super().__init__()
        self.fx_cross_code = fx_cross_code

    def _get_items(self):
        return [param_item.to_kv("fxCrossCode", self.fx_cross_code)]
