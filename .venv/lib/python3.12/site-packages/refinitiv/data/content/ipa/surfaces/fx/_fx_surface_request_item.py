from typing import Optional, TYPE_CHECKING

from ._fx_statistics_parameters import FxStatisticsParameters
from ._fx_surface_definition import FxVolatilitySurfaceDefinition as FxSurfaceDefinition
from ._fx_surface_parameters import FxSurfaceParameters as FxCalculationParams
from ..._enums import UnderlyingType
from .._surface_request_item import SurfaceRequestItem
from ..._param_item import serializable_param_item

if TYPE_CHECKING:
    from ....._types import OptStr


class FxSurfaceRequestItem(SurfaceRequestItem):
    # new name FxVolatilitySurfaceRequestItem into version 1.0.130
    def __init__(
        self,
        surface_layout=None,
        surface_parameters: Optional[FxCalculationParams] = None,
        underlying_definition: Optional[FxSurfaceDefinition] = None,
        surface_tag: "OptStr" = None,
        surface_statistics_parameters: Optional[FxStatisticsParameters] = None,
    ):
        super().__init__(
            surface_layout=surface_layout,
            surface_tag=surface_tag,
            underlying_type=UnderlyingType.FX,
        )
        self.surface_parameters = surface_parameters
        self.underlying_definition = underlying_definition
        self.surface_statistics_parameters = surface_statistics_parameters

    def _get_items(self):
        return super()._get_items() + [
            serializable_param_item.to_kv("surfaceParameters", self.surface_parameters),
            serializable_param_item.to_kv("underlyingDefinition", self.underlying_definition),
            serializable_param_item.to_kv("surfaceStatisticsParameters", self.surface_statistics_parameters),
        ]
