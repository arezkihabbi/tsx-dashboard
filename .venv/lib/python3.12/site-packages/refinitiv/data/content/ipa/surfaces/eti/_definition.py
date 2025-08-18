from typing import TYPE_CHECKING, Union, Optional

from ._eti_surface_request_item import EtiSurfaceRequestItem
from ..._content_provider_layer import IPAContentProviderLayer
from ...._content_provider_layer import PosArgsWarnMixin
from ....._content_type import ContentType

if TYPE_CHECKING:
    from .._models import SurfaceLayout
    from . import EtiCalculationParams, EtiSurfaceDefinition
    from ....._types import ExtendedParams, OptStr


class Definition(IPAContentProviderLayer, PosArgsWarnMixin):
    """
    Create a Eti data Definition object.

    Parameters
    ----------
    surface_layout : SurfaceLayout
        See details in SurfaceLayout class
    surface_parameters : EtiCalculationParams
        See details in EtiCalculationParams class
    underlying_definition : dict or EtiSurfaceDefinition
       Dict or EtiSurfaceDefinition object. See details in EtiSurfaceDefinition class
       Example:
            {"instrumentCode": "USD"}
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
    >>> from refinitiv.data.content.ipa.surfaces import eti
    >>> definition = eti.Definition(
    ...     underlying_definition=eti.EtiSurfaceDefinition(instrument_code="USD"),
    ...     surface_tag="USD_Strike__Tenor_",
    ...     surface_layout=eti.SurfaceLayout(
    ...         format=eti.Format.MATRIX
    ...     ),
    ...     surface_parameters=eti.EtiCalculationParams(
    ...         x_axis=eti.Axis.TENOR,
    ...         y_axis=eti.Axis.STRIKE,
    ...         calculation_date="2020-03-20"
    ...     )
    >>> )
    """

    _WARN_NAME = "surfaces.eti.Definition"
    _WARN_EX = "use surfaces.eti.Definition(surface_tag='USD_Strike__Tenor_') instead of surfaces.eti.Definition('USD_Strike__Tenor_')"

    def __init__(
        self,
        surface_layout: "SurfaceLayout" = None,
        surface_parameters: Optional["EtiCalculationParams"] = None,
        underlying_definition: Union[dict, "EtiSurfaceDefinition"] = None,
        surface_tag: "OptStr" = None,
        extended_params: "ExtendedParams" = None,
    ):
        request_item = EtiSurfaceRequestItem(
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
