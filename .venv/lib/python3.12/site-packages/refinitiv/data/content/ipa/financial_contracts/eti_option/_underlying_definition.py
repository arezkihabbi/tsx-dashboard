from typing import Optional

from ..._param_item import param_item
from ..._serializable import Serializable


class EtiUnderlyingDefinition(Serializable):
    """
    Parameters
    ----------
    instrument_code : str, optional
        The underlier RIC
    """

    def __init__(
        self,
        instrument_code: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.instrument_code = instrument_code

    def _get_items(self):
        return [
            param_item.to_kv("instrumentCode", self.instrument_code),
        ]
