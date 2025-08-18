from typing import Optional

from ..._param_item import param_item
from ..._serializable import Serializable


class EtiCbbcDefinition(Serializable):
    """
    Parameters
    ----------
    conversion_ratio : float, optional

    level : float, optional

    """

    def __init__(
        self,
        conversion_ratio: Optional[float] = None,
        level: Optional[float] = None,
    ) -> None:
        super().__init__()
        self.conversion_ratio = conversion_ratio
        self.level = level

    def _get_items(self):
        return [
            param_item.to_kv("conversionRatio", self.conversion_ratio),
            param_item.to_kv("level", self.level),
        ]
