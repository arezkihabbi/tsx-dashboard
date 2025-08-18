from .._surface_request_item import SurfaceRequestItem
from ..._enums import UnderlyingType
from ..._param_item import serializable_param_item


class CapSurfaceRequestItem(SurfaceRequestItem):
    # new name CapletsStrippingSurfaceRequestItem in version 1.0.130
    def __init__(
        self,
        instrument_type,
        surface_layout,
        surface_params,
        underlying_definition,
        surface_tag,
    ):
        super().__init__(
            surface_layout=surface_layout,
            surface_tag=surface_tag,
            underlying_type=UnderlyingType.CAP,
        )
        self.instrument_type = instrument_type
        self.surface_parameters = surface_params
        self.underlying_definition = underlying_definition

    def _get_items(self):
        return super()._get_items() + [
            serializable_param_item.to_kv("surfaceParameters", self.surface_parameters),
            serializable_param_item.to_kv("underlyingDefinition", self.underlying_definition),
        ]
