import warnings
from typing import TYPE_CHECKING, Union, Optional

from ._cap_surface_request_item import CapSurfaceRequestItem
from ..._content_provider_layer import IPAContentProviderLayer
from ...._content_provider_layer import PosArgsWarnMixin
from ....._content_type import ContentType

if TYPE_CHECKING:
    from .._models import SurfaceLayout
    from . import CapSurfaceDefinition, CapCalculationParams
    from ....._types import ExtendedParams, OptStr


class Definition(IPAContentProviderLayer, PosArgsWarnMixin):
    """
    Create a Cap data Definition object.

    Parameters
    ----------
    surface_layout : SurfaceLayout
        See details in SurfaceLayout class
    surface_parameters : CapCalculationParams
        See details in CapCalculationParams class
    underlying_definition : dict or CapSurfaceDefinition
       Dict or CapSurfaceDefinition object. See details in CapSurfaceDefinition class
       Example:
            {"instrumentCode": "USD"}
    surface_tag : str, optional
        A user defined string to describe the volatility surface
    instrument_type : DEPRECATED
        This attribute doesn't use anymore.
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
    >>> from refinitiv.data.content.ipa.surfaces import cap
    >>> definition = cap.Definition(
    ...     underlying_definition=cap.CapSurfaceDefinition(
    ...         instrument_code="USD",
    ...         reference_caplet_tenor="3M",
    ...         discounting_type=cap.DiscountingType.OIS_DISCOUNTING
    ...     ),
    ...     surface_tag="USD_Strike__Tenor_",
    ...     surface_layout=cap.SurfaceLayout(
    ...         format=cap.Format.MATRIX
    ...     ),
    ...     surface_parameters=cap.CapCalculationParams(
    ...         x_axis=cap.Axis.STRIKE,
    ...         y_axis=cap.Axis.TENOR,
    ...         calculation_date="2020-03-20"
    ...     )
    >>> )
    """

    _WARN_NAME = "surfaces.cap.Definition"
    _WARN_EX = "use surfaces.cap.Definition(surface_tag='USD_Strike__Tenor_') instead of surfaces.cap.Definition('USD_Strike__Tenor_')"

    def __init__(
        self,
        surface_layout: "SurfaceLayout" = None,
        surface_parameters: Optional["CapCalculationParams"] = None,
        underlying_definition: Union[dict, "CapSurfaceDefinition"] = None,
        surface_tag: "OptStr" = None,
        instrument_type=None,
        extended_params: "ExtendedParams" = None,
    ):
        if instrument_type is not None:
            warnings.warn(
                "The 'instrument_type' parameter for rd.content.ipa.surfaces.cap.Definition class "
                "will be removed in future library version v2.0. "
                "This parameter is not supported by the back-end anymore.",
                category=FutureWarning,
            )
        request_item = CapSurfaceRequestItem(
            instrument_type=instrument_type,
            surface_layout=surface_layout,
            surface_params=surface_parameters,
            underlying_definition=underlying_definition,
            surface_tag=surface_tag,
        )
        super().__init__(
            content_type=ContentType.SURFACES,
            universe=request_item,
            extended_params=extended_params,
        )
