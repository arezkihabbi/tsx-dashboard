from typing import TYPE_CHECKING, Union

from ..._content_provider_layer import IPAContentProviderLayer
from ._fx_surface_request_item import FxSurfaceRequestItem
from ...._content_provider_layer import PosArgsWarnMixin
from ....._content_type import ContentType
from ....._tools import create_repr

if TYPE_CHECKING:
    from ._fx_surface_parameters import FxSurfaceParameters
    from .._models import SurfaceLayout
    from . import FxSurfaceDefinition
    from ....._types import ExtendedParams, OptStr


class Definition(IPAContentProviderLayer, PosArgsWarnMixin):
    """
    Create a Fx data Definition object.

    Parameters
    ----------
    surface_layout : SurfaceLayout
        See details in SurfaceLayout class
    surface_parameters : SurfaceParameters
        See details in SurfaceParameters class
    underlying_definition : dict or FxSurfaceDefinition
       Dict or FxSurfaceDefinition object. See details in FxSurfaceDefinition class
       Example:
            {"fxCrossCode": "EURUSD"}
    surface_tag : str, optional
        A user defined string to describe the volatility surface
    extended_params : dict, optional
        If necessary other parameters

    Methods
    -------
    get_data(session=session, on_response=on_response, **kwargs)
        Returns a response to the data platform
    get_data_async(session=None, on_response=None, **kwargs)
        Returns a response asynchronously to the data platform

    Examples
    --------
    >>> from refinitiv.data.content.ipa.surfaces import fx
    >>> definition = fx.Definition(
    ...    underlying_definition={"fxCrossCode": "EURUSD"},
    ...    surface_tag="FxVol-EURUSD",
    ...    surface_layout=fx.SurfaceLayout(
    ...    format=fx.Format.MATRIX
    ...    ),
    ...    surface_parameters=fx.FxCalculationParams(
    ...    x_axis=fx.Axis.DATE,
    ...    y_axis=fx.Axis.STRIKE,
    ...    calculation_date="2018-08-20T00:00:00Z"
    ...    )
    ...)
    >>>
    """

    _WARN_NAME = "surfaces.fx.Definition"
    _WARN_EX = (
        "use surfaces.fx.Definition(surface_tag='FxVol-EURUSD') instead of surfaces.fx.Definition('FxVol-EURUSD')"
    )

    def __init__(
        self,
        surface_layout: "SurfaceLayout" = None,
        surface_parameters: "FxSurfaceParameters" = None,
        underlying_definition: Union[dict, "FxSurfaceDefinition"] = None,
        surface_tag: "OptStr" = None,
        extended_params: "ExtendedParams" = None,
    ):
        request_item = FxSurfaceRequestItem(
            surface_layout=surface_layout,
            surface_parameters=surface_parameters,
            underlying_definition=underlying_definition,
            surface_tag=surface_tag,
        )
        super().__init__(
            content_type=ContentType.SURFACES,
            universe=request_item,
            extended_params=extended_params,
        )

    def __repr__(self):
        return create_repr(self)
