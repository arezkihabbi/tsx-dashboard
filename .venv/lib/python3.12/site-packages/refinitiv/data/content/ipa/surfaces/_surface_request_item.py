from .._enums import UnderlyingType
from ._models import SurfaceLayout
from .._param_item import serializable_param_item, enum_param_item, param_item

from .._serializable import Serializable


class SurfaceRequestItem(Serializable):
    def __init__(
        self,
        surface_layout: SurfaceLayout,
        surface_tag: str,
        underlying_type: UnderlyingType,
    ):
        super().__init__()
        self.surface_tag = surface_tag
        self.surface_layout = surface_layout
        self.underlying_type = underlying_type

    def _get_items(self):
        return [
            serializable_param_item.to_kv("surfaceLayout", self.surface_layout),
            enum_param_item.to_kv("underlyingType", self.underlying_type),
            param_item.to_kv("surfaceTag", self.surface_tag),
        ]
