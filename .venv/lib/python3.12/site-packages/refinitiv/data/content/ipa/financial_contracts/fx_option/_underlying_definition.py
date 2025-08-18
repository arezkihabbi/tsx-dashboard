from typing import Optional

from ..._param_item import param_item
from ..._serializable import Serializable


class FxUnderlyingDefinition(Serializable):
    """
    Parameters
    ----------
    fx_cross_code : str, optional
        The currency pair. Should contain the two currencies, ex EURUSD
    """

    def __init__(
        self,
        fx_cross_code: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.fx_cross_code = fx_cross_code

    def _get_items(self):
        return [
            param_item.to_kv("fxCrossCode", self.fx_cross_code),
        ]
