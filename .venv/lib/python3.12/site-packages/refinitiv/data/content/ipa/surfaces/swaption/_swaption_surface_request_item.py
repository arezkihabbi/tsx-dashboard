from ..._enums import UnderlyingType
from .._surface_request_item import SurfaceRequestItem
from ._swaption_calculation_params import SwaptionCalculationParams
from ._swaption_surface_definition import SwaptionSurfaceDefinition
from ..._param_item import serializable_param_item


class SwaptionSurfaceRequestItem(SurfaceRequestItem):
    # new name VolatilityCubeSurfaceRequestItem in version 1.0.130

    def __init__(
        self,
        instrument_type=None,
        surface_layout=None,
        surface_parameters: SwaptionCalculationParams = None,
        underlying_definition: SwaptionSurfaceDefinition = None,
        surface_tag=None,
    ):
        super().__init__(
            surface_layout=surface_layout,
            surface_tag=surface_tag,
            underlying_type=UnderlyingType.SWAPTION,
        )
        self.instrument_type = instrument_type
        self.surface_parameters = surface_parameters
        self.underlying_definition = underlying_definition

    def _get_items(self):
        return super()._get_items() + [
            serializable_param_item.to_kv("surfaceParameters", self.surface_parameters),
            serializable_param_item.to_kv("underlyingDefinition", self.underlying_definition),
        ]
