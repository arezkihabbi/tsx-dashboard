from typing import Optional

from ._barrier_definition import EtiBarrierDefinition
from ..._param_item import list_serializable_param_item
from ..._serializable import Serializable


class EtiDoubleBarriersDefinition(Serializable):
    """
    Parameters
    ----------
    barriers_definition : EtiBarrierDefinition, optional

    """

    def __init__(
        self,
        barriers_definition: Optional[EtiBarrierDefinition] = None,
    ) -> None:
        super().__init__()
        self.barriers_definition = barriers_definition

    def _get_items(self):
        return [
            list_serializable_param_item.to_kv("barriersDefinition", self.barriers_definition),
        ]
