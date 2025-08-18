from ._eti_surface_definition import EtiSurfaceDefinition
from ._eti_surface_parameters import EtiSurfaceParameters as EtiCalculationParams
from .._surface_request_item import SurfaceRequestItem
from ..._enums import UnderlyingType
from ..._param_item import serializable_param_item


class EtiSurfaceRequestItem(SurfaceRequestItem):
    # new name EtiVolatilitySurfaceRequestItem into version 1.0.130
    def __init__(
        self,
        surface_layout,
        surface_parameters: EtiCalculationParams,
        underlying_definition: EtiSurfaceDefinition,
        surface_tag: str,
    ):
        super().__init__(
            surface_layout=surface_layout,
            surface_tag=surface_tag,
            underlying_type=UnderlyingType.ETI,
        )
        self.surface_parameters = surface_parameters
        self.underlying_definition = underlying_definition

    def _get_items(self):
        return super()._get_items() + [
            serializable_param_item.to_kv("surfaceParameters", self.surface_parameters),
            serializable_param_item.to_kv("underlyingDefinition", self.underlying_definition),
        ]
